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
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains



class PieLegendComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()




    def setSelectionIndex(self,driverHelper,index,elHandle):
        '''
        This method send click action to a specified index
        :param index: index to be selected
        :param elHandle: handler to CheckBox Column
        :return: nothing
        '''
        for i in range(0,len(elHandle)):
            # time.sleep(2)
            if i in index:
                # driverHelper.action.move_to_element(elHandle[i]).key_down(Keys.COMMAND).click().key_up(Keys.COMMAND).perform()
                # driverHelper.action.release().perform()
                try:
                    elHandle[i].click()
                    return True
                except Exception:
                    return Exception

                # break

    def getSelectionIndex(self,elHandle):
        '''
        This method gives the Selected Index of the BarChart
        :param elHandle: Handler to CheckBox Column
        :return: Selected Index
        '''
        selIndices = []
        for i in range(0,len(elHandle)):
            if "selected" in elHandle[i].get_attribute('class') :
                selIndices.append(i)
        return selIndices


    def getData(self,handlrs):
        '''
        Returns Data as Dictionary with Name and Value
        :param handlers: Handlers to all the components
        :return: Data from the Bar Chart
        '''
        data = {}
        handlers = self.compHandlers('pielegend',handlrs)
        print "handle of get data",handlers
        data['legendText'] = [ele.text for ele in handlers['legendText']]
        # for i in range(len(handlers['legendText'])):
        #     data['legendText'] = handlers['legendText'][i].text

        tempArr = []
        for i in range(len(handlers['legendIcon'])):
            for child in handlers['legendIcon'][i].find_elements_by_xpath(".//*"):
                if child.get_attribute("class") == "circle":
                    tempArr.append(child.value_of_css_property('background-color'))
        data['legendIcon'] =tempArr
        return data

    def setSelection(self,driverHelper,indices,handlrs,comp=None):
        '''
        This method do the Selection on the Bar Chart as per the index supplied
        :param indices: indices to be selected
        :param handlers: Handlers to BarChart
        :return: True/False
        '''
        # handlers = self.compHandlers('pielegend',handlrs)
        handlers = handlrs['pielegend']
        selectedIndex = self.getSelectionIndex(handlers['legendText'])
        if selectedIndex in indices:
            return True
        else:
            return self.setSelectionIndex(driverHelper,indices,handlers['legendText'])

    def getData1(self,handlers,parent,child=None):
        '''
        Returns Data as Dictionary with Name and Value
        :param handlers: Handlers to all the components
        :return: Data from the Bar Chart
        '''
        data = {}
        if child == None:
            child = 'legendText'
        # handlers = self.compHandlers('pielegend',handlrs)
        # print "handle of get data",handlers
        data['legendText'] = [ele.text for ele in handlers[parent][child]]
        # for i in range(len(handlers['legendText'])):
        #     data['legendText'] = handlers['legendText'][i].text

        tempArr = []
        for i in range(len(handlers[parent]['legendIcon'])):
            for child in handlers[parent]['legendIcon'][i].find_elements_by_xpath(".//*"):
                if child.get_attribute("class") == "circle":
                    tempArr.append(child.value_of_css_property('background-color'))
        data['legendIcon'] =tempArr
        return data

    def setSelection1(self,driverHelper,indices,handlrs,parent,child=None):
        '''
        This method do the Selection on the Bar Chart as per the index supplied
        :param indices: indices to be selected
        :param handlers: Handlers to BarChart
        :return: True/False
        '''
        if child == None:
            child = 'legendText'
        selectedIndex = self.getSelectionIndex(handlrs[parent][child])
        if selectedIndex in indices:
            return True
        else:
            return self.setSelectionIndex(driverHelper,indices,handlrs[parent][child])


    def getSelection1(self,handlrs,parent,child=None):
        '''
        This method gives the selected Index, its Corresponding Text and Value
        :param handlers: handler to pieChart
        :return: Selected Data
        '''
        try:
            data = {}
            if child == None:
                child = 'legendText'

            # handlers = self.compHandlers('pielegend',handlrs)
            data['selIndices'] = self.getSelectionIndex(handlrs[parent][child])
            data['legendText'] = [handlrs[parent][child][ele].text for ele in data['selIndices']]
            return data
        except Exception:
            return Exception

    def getSelection(self,handlrs):
        '''
        This method gives the selected Index, its Corresponding Text and Value
        :param handlers: handler to pieChart
        :return: Selected Data
        '''
        try:
            data = {}
            handlers = self.compHandlers('pielegend',handlrs)
            data['selIndices'] = self.getSelectionIndex(handlers['legendText'])
            data['legendText'] = [handlers['legendText'][ele].text for ele in data['selIndices']]
            # data['legendText'] = handlers['legendText'][data['selIndices']].text
            # data['legendIcon'] = handlers['legendIcon'][data['selIndex']].color # dummy line will update
            return data
        except Exception:
            return Exception


    def launchToolTip(self,driver,driverHelper,elHandle):
        '''
        This method gives the Selected Index of the BarChart
        :param elHandle: Handler to CheckBox Column
        :return: Selected Index
        '''
        data = []
        # driverHelper.action.move_to_element()
        for i in range(0,len(elHandle['hover'])):
            driverHelper.action.move_to_element(elHandle['hover'][i]).perform()
            # adding hardcoded timeout (will be driven by Config)
            time.sleep(2)
            data.append(elHandle['getToolTipData'][0].text)
        return data

    def getToolTipInfo(self,driver,driverHelper,handlrs):
        '''

        :param tipHandle:
        :return:
        '''
        data = []
        handlers = self.compHandlers('btv',handlrs)

        toolTipHandlers = {}
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "hover":
                toolTipHandlers['hover'] = value
            elif self.configmanager.componentSelectors[key]["action"] == "getToolTipData":
                toolTipHandlers['getToolTipData'] = value
        return self.launchToolTip(driver,driverHelper,toolTipHandlers)

    def validateToolTipData(self,dataCollection):

        finalTTD = {}
        total = False
        for i in range(1,len(dataCollection['btvTooltipData'])):
            ttd = {}
            stdd = {}
            subStrings = dataCollection['btvTooltipData'][i].split('\n')
            ar = []

            for i in range(1,len(subStrings)):
                ar.append(subStrings[i])
            ttd[subStrings[0]] = ar

            for key,value in ttd.iteritems():
                for el in value:
                    stdd[el.split(":")[0]]= float(el.split(":")[1].strip().split(" ")[0])

            if len(stdd) ==2:
                total = True
                s = 0
                for k,v in stdd.iteritems():
                    s+=v
                stdd["Total "+el.split(":")[0].split(" ")[1]] = s
            else:
                total = False

            finalTTD[subStrings[0]] = stdd
        result = {}
        for key,value in finalTTD.iteritems():
            UIData = 0.0
            UIData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])

            if total:
                for k in value.keys():
                    if "Total" in k:
                        if value[k] == UIData:
                            result[key] = "Tooltip Validation PASSED"
                        else:
                            result[key] = "Tooltip Validation FAILED"

        return result
