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


from QuicklinkTimeRangeComponentClass import QuicklinkTimeRangeComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.ConfigManager import ConfigManager
import time

from selenium.webdriver import ActionChains



class TimeRangeComponentClass(QuicklinkTimeRangeComponentClass):

    def __init__(self):
        QuicklinkTimeRangeComponentClass.__init__(self)


    def setCustomTime(self,date,h,parent="timeRangeDiv",child="cal"):
        # Activate
        h[parent][child][len(h[parent][child])-1].click()


