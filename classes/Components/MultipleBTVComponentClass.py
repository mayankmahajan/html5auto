#!/usr/bin/env python
##############################################################
'''
BarTabular Component Handler
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################



from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *
from Utils.resultlogger import *
from Utils.UnitSystem import *

from selenium.webdriver import ActionChains



class MultipleBTVComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()



    def getDataforColumn(self,elHandle,indices=[]):
        return [el.text for el in elHandle.find_elements_by_tag_name("text")]

    def setSelectionIndex(self,index,elements):
        try:
            elHandle = elements.find_elements_by_css_selector("input")
            logger.info("Got %s checkboxes on BTV to select",str(len(elHandle)))
            logger.info("Going to select indices on BTV = %s",str(index))
            for i in range(1,len(elHandle)):
                if i in index:
                    logger.info("Going to select index on BTV = %s",str(i))
                    elHandle[i].click()
                    logger.info("Index on BTV is clicked = %s",str(i))
            return True
        except Exception as e:
            logger.error("Got Exception while setting selection for index %s = %s",str(i),str(e))
            return e

    def getSelection(self,elements,returnText=False):
        indices = []
        elHandle = elements.find_elements_by_tag_name("div")
        for i in range(len(elHandle)):
            if "255" not in elHandle[i].value_of_css_property('background-color') :
                indices.append(str(elHandle[i].text).strip().strip("\n").strip() if returnText else i)
        return indices


    def getBTVData(self,setup,h,parent="btvGroup",child1="BTVCOLUMN1",child2="BTVCOLUMN2",occurence=0):

        if not h[parent][child1]:
            self.takeScreenshot(setup.d)
            return False
        if not h[parent][child2]:
            self.takeScreenshot(setup.d)
            return False
        data = {}
        data[child1] = self.getData(h,child=child1,occurence=occurence)
        data[child2] = self.getData(h,child=child2,occurence=occurence)

        logger.debug("Selected btv data = %s",str(data))
        return data

    def getData(self,handlrs,parent="btvGroup",child="BTVCOLUMN1",occurence=0):
        data = {}
        handlers = handlrs[parent][child][occurence]
        return self.getDataforColumn(handlers)

    def setSelection(self,setup,index,h,parent="btvGroup",child="BTVCOLUMN0",occurence=0):
        if not h[parent][child]:
            self.takeScreenshot(setup.d)
            return False
        return self.setSelectionIndex(index,h[parent][child][occurence])

    def getSelections(self,setup,h,parent="btvGroup",child1="BTVCOLUMN0",child2="BTVCOLUMN1",child3="BTVCOLUMN2",occurence=0,measureSelected=""):

        if not h[parent][child1]:
            self.takeScreenshot(setup.d)
            return False
        if not h[parent][child2]:
            self.takeScreenshot(setup.d)
            return False
        if not h[parent][child3]:
            self.takeScreenshot(setup.d)
            return False

        data = {}
        data['selIndices']=self.getSelection(h[parent][child1][occurence])
        data['dim'] = self.getSelection(h[parent][child2][occurence],returnText=True)
        data['value'] = self.getSelection(h[parent][child3][occurence],returnText=True)

        # if "Flows" in measureSelected and len(data['value'])!=0:
        #     data['totalValue']=self.totalvalueformlist(data['value'],unitValue=1000)
        # elif "Avg" in measureSelected and len(data['value'])!=0:
        #     data['totalValue']=self.totalvalueformlist(data['value'],flag="avg",unitValue=60)
        # elif len(data['value'])!=0:
        #     data['totalValue'] = self.totalvalueformlist(data['value'])
        # else:
        #     data['totalValue'] = ""
        #
        # data['dimSelected'] =""
        # if len(data['dim'])!=0:
        #     for dim in data['dim']:
        #         if data['dimSelected']=="":
        #             data['dimSelected']=str(dim)
        #         else:
        #             data['dimSelected']=data['dimSelected']+","+str(dim)


        return self.merge_dictionaries(data,self.calTotal(data['dim'],data['value'],measureSelected))

        # return data




    def launchToolTip(self,driverHelper,elHandle):
        data = []
        for i in range(0,len(elHandle['hover'])):
            driverHelper.action.move_to_element(elHandle['hover'][i]).perform()
            # adding hardcoded timeout (will be driven by Config)
            time.sleep(2)
            data.append(elHandle['getToolTipData'][0].text)
        return data

    def getToolTipInfo(self,setup,h,parent="btvGroup",child="BTVHOVERAREA",child_tooltip="BTVTOOLTIP",occurence=0):
        '''

        :param tipHandle:
        :return:
        '''
        data = []
        toolTipHandlers = {}
        handlers = h[parent][child][occurence]
        toolTipHandlers['hover'] = handlers.find_elements_by_css_selector("rect[class*=bar]")
        toolTipHandlers['getToolTipData'] = handlers.find_elements_by_css_selector("div#barTabularChartToolTip")
        return self.launchToolTip(setup.dH,toolTipHandlers)

    # added for Content Mural Screen
    def getHeader(self,h,index="",parent="btvGroup",child="selectionlabel"):
        return str(h[parent][child][0].text.strip().strip('\n').strip())
