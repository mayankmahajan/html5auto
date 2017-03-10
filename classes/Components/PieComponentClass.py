#!/usr/bin/env python
##############################################################
'''
Pie Component Handler
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

from selenium.webdriver import ActionChains



class PieComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()




    def setSelectionIndex(self,index,elHandle):
        '''
        This method send click action to a specified index
        :param index: index to be selected
        :param elHandle: handler to CheckBox Column
        :return: nothing
        '''
        for i in range(0,len(elHandle)):
            if i == index:
                elHandle[i].click()
                break

    def getSelectionIndex(self,elHandle):
        '''
        This method gives the Selected Index of the BarChart
        :param elHandle: Handler to CheckBox Column
        :return: Selected Index
        '''
        for i in range(0,len(elHandle)):
            if "selected" in elHandle[i].get_attribute('class') :
                return i


    # def getData(self,handlrs):
    #     '''
    #     Returns Data as Dictionary with Name and Value
    #     :param handlers: Handlers to all the components
    #     :return: Data from the Bar Chart
    #     '''
    #     data = {}
    #     handlers = self.compHandlers('pielegend',handlrs)
    #
    #     data['legendText'] = [ele.text for ele in handlers['legendText']]
    #     # for i in range(len(handlers['legendText'])):
    #     #     data['legendText'] = handlers['legendText'][i].text
    #
    #     tempArr = []
    #     for i in range(len(handlers['legendIcon'])):
    #         for child in handlers['legendIcon'][i].find_elements_by_xpath(".//*"):
    #             if child.get_attribute("class") == "circle":
    #                 tempArr.append(child.value_of_css_property('background-color'))
    #     data['legendIcon'] =tempArr
    #
    #
    #
    #
    #
    #     return data

    def setSelection(self,index,handlrs,force=False):
        '''
        This method do the Selection on the Bar Chart as per the index supplied
        :param index: Index to be selected
        :param handlers: Handlers to BarChart
        :return: True/False
        '''
        handlers = self.compHandlers('pielegend',handlrs)
        selectedIndex = self.getSelectionIndex(handlers['legendText'])
        if not force and selectedIndex == index :
            return True
        else:
            self.setSelectionIndex(index,handlers['legendText'])

    # def getSelection(self,handlrs):
    #     '''
    #     This method gives the selected Index, its Corresponding Text and Value
    #     :param handlers: handler to pieChart
    #     :return: Selected Data
    #     '''
    #     try:
    #         data = {}
    #         handlers = self.compHandlers('piechart',handlrs)
    #         data['selIndex'] = self.getSelectionIndex(handlers['legendText'])
    #         data['legendText'] = handlers['legendText'][data['selIndex']].text
    #         data['legendIcon'] = handlers['legendIcon'][data['selIndex']].color # dummy line will update
    #         return data
    #     except Exception:
    #         return Exception


    def launchToolTip(self,driver,driverHelper,elHandle):
        '''
        This method gives the Selected Index of the BarChart
        :param elHandle: Handler to CheckBox Column
        :return: Selected Index
        '''
        data = []
        # driverHelper.action.move_to_element()
        for i in range(0,len(elHandle['hover'])):
            # print "element",elHandle['hover'][i]
            try:
                driverHelper.action.move_to_element(elHandle['hover'][i]).perform()
            except:
                pass
            # adding hardcoded timeout (will be driven by Config)
            time.sleep(2)
            data.append(elHandle['getToolTipData'].text)
        return data

    def getPieSelections(self,handlrs):
        '''

        :param handlrs:
        :return:
        '''
        handlers = self.compHandlers('piechart',handlrs)
        return [ele.get_attribute('data-index') for ele in handlers['wedgeselected']]

        # sels = []
        # for ele in handlers['wedgeselected']:
        #     sels.append(ele.get_attribute('data-index'))
        # return sels

    def getToolTipInfo(self,driver,driverHelper,handlrs):
        '''

        :param tipHandle:
        :return:
        '''
        data = []
        toolTipHandlers = {}
        handlers = self.compHandlers('piechart',handlrs)
        # print "tool tip handler"
        # print handlers
        toolTipHandlers['hover'] = [handlers['arcs'][i] for i in range(len(handlers['arcs']))]
            # if handlers['arcs'][i].tag_name == "path":
            #     toolTipHandlers['hover'] = handlers['arcs'][i]

                # and ele.value_of_css_property('background-color') == "g":



        # for key,value in handlers.iteritems():
        #     if self.configmanager.componentSelectors[key]["action"] == "hover":
        #         toolTipHandlers['hover'] = value
        #     elif self.configmanager.componentSelectors[key]["action"] == "getToolTipData":
        toolTipHandlers['getToolTipData'] = handlers['tooltip'][0]
        print toolTipHandlers
        return self.launchToolTip(driver,driverHelper,toolTipHandlers)

    def getToolTipInfo1(self,driver,driverHelper,handlers,parent,child=None):
        '''

        :param tipHandle:
        :return:
        '''
        data = []
        toolTipHandlers = {}

        if child == None:
            child = 'arcs'
        # handlers = self.compHandlers('piechart',handlrs)
        # print "tool tip handler"
        # print handlers
        toolTipHandlers['hover'] = [handlers[parent][child][i] for i in range(len(handlers[parent][child]))]
        toolTipHandlers['getToolTipData'] = handlers[parent]['tooltip'][0]
        return self.launchToolTip(driver,driverHelper,toolTipHandlers)





    # def validateToolTipData(self,dataCollection):
    #
    #     for i in range(len(dataCollection['tooltipdata'])):
    #         if dataCollection['legendText'] == dataCollection['tooltipdata']:
    #             result[key] = "Tooltip Validation PASSED"
    #         else:
    #             result[key] = "Tooltip Validation FAILED"
    #
    #
    #
    #     finalTTD = {}
    #     total = False
    #     for i in range(1,len(dataCollection['tooltipdata'])):
    #         ttd = {}
    #         stdd = {}
    #         subStrings = dataCollection['tooltipdata'][i].split('\n')
    #         ar = []
    #
    #         for i in range(1,len(subStrings)):
    #             ar.append(subStrings[i])
    #         ttd[subStrings[0]] = ar
    #
    #         for key,value in ttd.iteritems():
    #             for el in value:
    #                 stdd[el.split(":")[0]]= float(el.split(":")[1].strip().split(" ")[0])
    #
    #         if len(stdd) ==2:
    #             total = True
    #             s = 0
    #             for k,v in stdd.iteritems():
    #                 s+=v
    #             stdd["Total "+el.split(":")[0].split(" ")[1]] = s
    #         else:
    #             total = False
    #
    #         finalTTD[subStrings[0]] = stdd
    #     result = {}
    #     for key,value in finalTTD.iteritems():
    #         UIData = 0.0
    #         UIData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])
    #
    #         if total:
    #             for k in value.keys():
    #                 if "Total" in k:
    #                     if value[k] == UIData:
    #                         result[key] = "Tooltip Validation PASSED"
    #                     else:
    #                         result[key] = "Tooltip Validation FAILED"
    #
    #     return result

    def validateBTVData(self,dataCollection,csvData):
        result = {}
        # for key,value in csvData.iteritems():
        for key in dataCollection['btvData']['dimension']:
            if "All " in key or "Others" in key:
                pass
            else:
                UIData = 0.0
                convertedData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])
                unitString = dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[1]
                UIData = self.unitSystem.getRawValue(convertedData,unitString)

                if csvData[key]['AGGR_totalByteBuffer'] == UIData:
                    result[key] = "Data Validation PASSED"
                else:
                    result[key] = "Data Validation FAILED --> Actual : "+str(UIData)+" and Expected : "+str(csvData[key]['AGGR_totalByteBuffer'])

        return result

    def getPieSelectionText(self,h,parent='piechart',child='selectionText'):
        logger.info("Going to get Selection Text from Pie Chart")

        dim,value= str(h[parent][child][0].text),str(h[parent][child][1].text)
        logger.debug("Got Selection Text, Dimension = %s and Value = %s",dim,value)

        return dim,value