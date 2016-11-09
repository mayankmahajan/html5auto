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

            dimensionSelected = handlers['summaryBarTable'][len(handlers['summaryBarTable'])-1].find_elements_by_class_name("LeftCell")[0].text
            measures = [ele.text for ele in handlers['summaryBarTable'][len(handlers['summaryBarTable'])-1].find_elements_by_class_name("Row")]
            values = [ele.text for ele in handlers['summaryBarTable'][len(handlers['summaryBarTable'])-1].find_elements_by_class_name("BottomRow")]

            data[dimensionSelected] = dict(zip(measures,values))

            return data
        except Exception:
            return Exception

    def validateDataWithInsta(self,d1,d2):
        return True