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
from Utils.logger import *

from selenium.webdriver import ActionChains



class TimeRangeComponentClass(QuicklinkTimeRangeComponentClass):

    def __init__(self):
        QuicklinkTimeRangeComponentClass.__init__(self)


    def setCustomTime(self,date,h,parent="timeRangeDiv",child="cal"):
        # Activate
        h[parent][child][len(h[parent][child])-1].click()


    @staticmethod
    def getLabel(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to get TimeRange Label from KTRS")
            label= str(h[parent][child][0].find_elements_by_xpath("./*")[0].text)
            logger.info("Got TimeRange Label from KTRS = %s",label)
            return label
        except Exception as e:
            logger.error("Got Exception while getting selection label from KTRS = %s",str(e))
            return e

    @staticmethod
    def launchCalendar(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to launch Calendar from KTRS")
            h[parent][child][0].find_elements_by_xpath("./*")[1].click()
            logger.info("Launch Calendar icon clicked successfully")
            return True
        except Exception as e:
            logger.error("Got Exception while clicking Calendar icon from KTRS = %s",str(e))
            return e


    @staticmethod
    def setQuickLink(value,h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to click quicklink from KTRS = %s",str(value))
            quicklinkHandlers = h[parent][child][0].find_elements_by_xpath("./*")[2]
            quickLinkToClick = quicklinkHandlers.find_elements_by_xpath('//a[contains(text(), "' + value + '")]')
            logger.info("Got Quicklink(s) with text = %s on the KTRS = %d ",str(value),len(quickLinkToClick))
            logger.info("Going to click on Quicklink = %s",str(quickLinkToClick[0].text))
            quickLinkToClick[0].click()
            logger.info("Quicklink clicked successfully")
            return True
        except Exception as e:
            logger.error("Got Exception while clicking quicklink = %s from KTRS = %s",str(value),str(e))
            return e

    @staticmethod
    def getSelectedQuickLink(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to getSelectedQuickLink from KTRS")
            quicklinkHandlers = h[parent][child][0].find_elements_by_xpath("./*")[2]
            selectedQuickLink = str(quicklinkHandlers.find_elements_by_css_selector("a[class=timeRangeSelectedText]")[0].text)
            logger.info("Got SelectedQuickLink from KTRS = %s",selectedQuickLink)
            return selectedQuickLink
        except Exception as e:
            logger.error("Got Exception while fetching Selected Quicklink = %s",str(e))
            return e


    def getAvailableTimeRange(self):
        st = self.configmanager.getNodeElements("availabletimerange","starttime")
        et = self.configmanager.getNodeElements("availabletimerange","endtime")
        return st,et