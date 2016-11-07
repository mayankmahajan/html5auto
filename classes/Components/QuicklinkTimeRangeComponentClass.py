#!/usr/bin/env python
##############################################################
'''
QuickLink TimeRange Component Handler
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



class QuicklinkTimeRangeComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()



    def setSelection(self,quicklink,handlrs):
        '''
        This method do the Selection on the Bar Chart as per the index supplied
        :param index: Index to be selected
        :param handlers: Handlers to BarChart
        :return: True/False
        '''
        handlers = self.compHandlers('timeRangeDiv',handlrs)
        self.setSelectionIndex(quicklink,handlers[str(quicklink)])


    def setSelectionIndex(self,quicklink,elHandle):
        '''
        This method send click action to a specified index
        :param index: index to be selected
        :param elHandle: handler to CheckBox Column
        :return: nothing
        '''
        elHandle[0].click()
