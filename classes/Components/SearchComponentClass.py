#!/usr/bin/env python
##############################################################
'''
Input Box Component Handler
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



class SearchComponentClass(BaseComponentClass):

    def getSearchText(self,handlrs):
        try:
            return handlrs['searchInput'][len(handlrs['searchInput'])-1].text
        except Exception:
            return Exception

    def setSearchText(self, handlrs, value):
        try:
            # handlers = self.compHandlers('search',handlrs)
            self.m_send_keys(handlrs['searchInput'][len(handlrs['searchInput'])-1], value)
            return True
        except Exception:
            return Exception


    def hitSearchIcon(self, handlrs):
        self.m_click(handlrs['searchIcon'][len(handlrs['searchIcon'])-1])