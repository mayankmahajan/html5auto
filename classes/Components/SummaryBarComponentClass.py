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
            # valuehandlers = summaryBarHandler.find_elements_by_class_name("BottomRow")


            dimensionSelected = summaryBarHandler.find_elements_by_class_name("LeftCell")[0].text
            measures = [ele.text for ele in summaryBarHandler.find_elements_by_class_name("Row")]

            d = {}
            for i in range(len(summaryBarHandler.find_elements_by_class_name("BottomRow"))):
                d[measures[i]] = {}
                # d[measures[i]]['Average'] = []
                # d[measures[i]]['Peak'] = []
                selectedOption=self.selectDropDownByText(summaryBarHandler.find_elements_by_tag_name("select")[i],"Average","Total")
                temp={}
                temp['Average'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text
                d[measures[i]]['Average'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text

                selectedOption=self.selectDropDownByText(summaryBarHandler.find_elements_by_tag_name("select")[i],"Peak")
                temp['Peak'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text
                d[measures[i]]['Peak'] = summaryBarHandler.find_elements_by_class_name("BottomRow")[i].text

            # values = [ele.text for ele in summaryBarHandler.find_elements_by_class_name("BottomRow")]
            # dropDownList = [ele.text for ele in summaryBarHandler.find_elements_by_tag_name("select")]


            # data[dimensionSelected] = dict(zip(measures,values))
            data[dimensionSelected] = d

            return data
        except Exception:
            return Exception

    # def set

    def validateDataWithInsta(self,d1,d2):
        return True