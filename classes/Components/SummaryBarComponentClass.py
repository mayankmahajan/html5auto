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
                if "Peak" in el.text or "Average" in el.text or "Total" in el.text:
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
        except Exception:
            return Exception

    # def set

    def validateDataWithInsta(self,d1,d2):
        return True