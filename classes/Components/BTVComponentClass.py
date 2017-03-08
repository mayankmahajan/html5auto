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

from selenium.webdriver import ActionChains



class BTVComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()



    def getDataforColumn(self,elHandle):
        '''
        This method is iterated for all the components with action getData
        :param elHandle: Handler to Column in BarChart
        :return: Data from BarChart
        '''
        return [eachHandler.text for eachHandler in elHandle]

    def setSelectionIndex(self,index,elHandle):
        '''
        This method send click action to a specified index
        :param index: index to be selected
        :param elHandle: handler to CheckBox Column
        :return: nothing
        '''
        for i in range(1,len(elHandle)):
            if i == index:
                elHandle[i].click()
                break


    def getDataforColumn1(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getDataForColumn2(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getSelectionIndex(self,elHandle):
        '''
        This method gives the Selected Index of the BarChart
        :param elHandle: Handler to CheckBox Column
        :return: Selected Index
        '''
        for i in range(1,len(elHandle)):
            if "255" not in elHandle[i].value_of_css_property('background-color') :
                return i


    def totalCheck(self,handlers):
        return True

    def getData1(self,handlers):
        c1 = self.getDataforColumn1(handlers[Constants.BTVCOLUMN1])
        c2 = self.getDataForColumn2(handlers[Constants.BTVCOLUMN2])
        data = dict(zip(c1,c2))
        return data

    def getData(self,handlrs,parent="btv"):
        '''
        Returns Data as Dictionary with Name and Value
        :param handlers: Handlers to all the components
        :return: Data from the Bar Chart
        '''
        data = {}
        handlers = self.compHandlers(parent,handlrs)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "getData":
                data[key] = self.getDataforColumn(value)
        return data

    def setSelection(self,index,handlrs,parent="btv"):
        '''
        This method do the Selection on the Bar Chart as per the index supplied
        :param index: Index to be selected
        :param handlers: Handlers to BarChart
        :return: True/False
        '''
        # handlers = self.compHandlers('btv',handlrs)
        handlers = handlrs[parent]
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "click":
                selectedIndex = self.getSelectionIndex(value)
                if selectedIndex == index:
                    return True
                else:
                    self.setSelectionIndex(index,value)
                    # self.setSelectionIndex(selectedIndex,value)

    def getSelection(self,handlrs,parent="btv"):
        '''
        This method gives the selected Index, its Corresponding Text and Value
        :param handlers: handler to barChart
        :return: Selected Data
        '''
        data = {}
        handlers = self.compHandlers(parent,handlrs)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "click":
                data['selIndex'] = self.getSelectionIndex(value)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "getData":
                if 'selIndex' in data:
                    data[key] = value[data['selIndex']].text
        return data

    # def compHandlers(self,handlers):
    #     return self.configmanager.componentChildRelations['btv']


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

    def getToolTipInfo(self,driver,driverHelper,handlrs,parent="btv"):
        '''

        :param tipHandle:
        :return:
        '''
        data = []
        handlers = self.compHandlers(parent,handlrs)

        toolTipHandlers = {}
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[parent][key]["action"] == "hover":
                toolTipHandlers['hover'] = value
            elif self.configmanager.componentSelectors[parent][key]["action"] == "getToolTipData":
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

    def validateToolTipData1(self,dataCollection):
        per = ""
        finalTTD = {}
        total = False
        for i in range(0,len(dataCollection['btvTooltipData'])):
            ttd = {}
            stdd = {}
            subStrings = dataCollection['btvTooltipData'][i].split('\n')
            ar = []

            for i in range(1,len(subStrings)):
                ar.append(subStrings[i])
            ttd[subStrings[0]] = ar

            for key,value in ttd.iteritems():
                for el in value:
                    print el.split(":")[1]
                    if '<' in el.split(":")[1]:
                        break
                    elif '%' in el.split(":")[1]:
                        per = el.split(":")[1]
                    else:
                        stdd[el.split(":")[0]]= float(el.split(":")[1].strip().split(" ")[0])
                    # print stdd[el.split(":")[0]]
            if (len(stdd) ==2) or (len(stdd) == 1):
                total = True
                s = 0
                for k,v in stdd.iteritems():
                    s+=v
                stdd["Total "+el.split(":")[0].split(" ")[1]] = s
            # elif len(stdd) == 1:
            #     total = True
            #     s = 0
            #     for k,v in stdd.iteritems():
            #         s+=v
            #     stdd["Total "+el.split(":")[0].split(" ")[1]] = s
            else:
                total = False



            finalTTD[subStrings[0]] = stdd
        result = {}
        if '%' in per:
            result[key] = False
        else:
            for key,value in finalTTD.iteritems():
                UIData = 0.0
                try:
                    UIData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])
                except:
                    UIData = ""
                    result[key] = True
                if total:
                    for k in value.keys():
                        if "Total" in k:
                            if value[k] == UIData:
                                result[key] = True
                            else:
                                result[key] = False
        if (all(value == True for value in result.values())):
            tooltip = True
        else:
            tooltip = False
        print tooltip
        return result[key]


    # added for network Mural Screen
    def getHeader(self,h,index,parent="btv",child="btv1"):
        return h[parent][child][index].find_elements_by_css_selector("[class*=PickerHeaderClass]")[0].text.strip().strip('\n').strip()
