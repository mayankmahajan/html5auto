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
from selenium.webdriver.support.select import Select
import time

from selenium.webdriver import ActionChains



class SummaryBarComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getSelection(self,handlrs):
        '''
        This method gives the selected Index, its Corresponding Text and Value
        :param handlers: handler to pieChart
        :return: Selected Data
        '''
        try:
            data = {}
            handlers = self.compHandlers('summarybar',handlrs)
            summaryBarHandler =handlers['summaryBarTable'][len(handlers['summaryBarTable'])-1]
            dimensionSelected = summaryBarHandler.find_elements_by_class_name("LeftCell")[0].text
            measures = [ele.text for ele in summaryBarHandler.find_elements_by_class_name("Row")]

            peakAvgHandlers=[]
            for el in summaryBarHandler.find_elements_by_tag_name("select"):
                if "Peak" in el.text or "Average" in el.text or "Total" in el.text or "total" in el.text:
                    peakAvgHandlers.append(el)


            d = {}
            for i in range(len(summaryBarHandler.find_elements_by_class_name("BottomRow"))):
                d[measures[i]] = {}
                selectedOption=self.selectDropDownByText(peakAvgHandlers[i],"Average","Total")
                temp={}
                d[measures[i]]['Average'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text
                selectedOption=self.selectDropDownByText(peakAvgHandlers[i],"Peak")
                d[measures[i]]['Peak'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text

            data[dimensionSelected] = d

            return data
        except Exception as e:
            return e


    # mural specific
    # method in progress will complete with coverage of network screen
    def getSelection1(self,setup,handlrs):
        '''
        This method gives the selected Index, its Corresponding Text and Value
        :param handlers: handler to pieChart
        :return: Selected Data
        '''
        try:
            data = {}
            options1 = setup.cM.getNodeElements("summaryCardOptions","option1")
            options2 = setup.cM.getNodeElements("summaryCardOptions","option2")
            handlers = self.compHandlers('summarybar',handlrs)
            summaryBarHandler =handlers['summaryBarTable'][len(handlers['summaryBarTable'])-1]
            dimensionSelected = summaryBarHandler.find_elements_by_class_name("LeftCell")[0].text
            measures = []
            cellinfo={}
            cellinfo[dimensionSelected]={}
            for eachcell in summaryBarHandler.find_elements_by_class_name("Cell"):
                childs=eachcell.find_elements_by_xpath("./*")
                l= len(childs)
                cellinfo[dimensionSelected][childs[0].text.strip()] # set karna hai
                if l ==4:
                    childs[3].text




            flag=0
            columnHandlers = []
            for ele in summaryBarHandler.find_elements_by_class_name("Row"):
                measures.append(ele.text)
                for e in ele.find_elements_by_tag_name("select"):
                    for x,value in options1.iteritems():
                        if value['locatorText'] in e.text:
                            flag = 1
                            break
                    if flag !=1:
                        for x,value in options2.iteritems():
                            if value['locatorText'] in e.text:
                                flag = 2
                                break

                    if flag==1:
                        columnHandlers['option1Handler'] = e

                    if flag==2:
                        columnHandlers['option2Handler'] = e

            peakAvgHandlers=[]
            for el in summaryBarHandler.find_elements_by_tag_name("select"):
                if "Peak" in el.text or "Average" in el.text or "Total" in el.text or "total" in el.text:
                    peakAvgHandlers.append(el)


            d = {}
            for i in range(len(summaryBarHandler.find_elements_by_class_name("BottomRow"))):
                d[measures[i]] = {}
                selectedOption=self.selectDropDownByText(peakAvgHandlers[i],"Average","Total")
                temp={}
                d[measures[i]]['Average'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text
                selectedOption=self.selectDropDownByText(peakAvgHandlers[i],"Peak")
                d[measures[i]]['Peak'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text

            data[dimensionSelected] = d

            return data
        except Exception as e:
            return e

    # def set

    def validateDataWithInsta(self,d1,d2):
        return True