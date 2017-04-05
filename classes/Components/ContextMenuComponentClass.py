#!/usr/bin/env python
##############################################################
'''
CM Component Handler
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################


from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.logger import *

class ContextMenuComponentClass(BaseComponentClass):
    def __init__(self):
        BaseComponentClass.__init__(self)
        self.utility = __import__("Utils.utility")

    def activateContextMenuOptions1(self,handle):
        handle['cm'][Constants.CONTEXTMENU][0].click()
    def activateContextMenuOptions(self,handle,parent="cm",child=Constants.CONTEXTMENU):
        try:
            logger.debug('Clicking Element :: Parent %s Child %s',parent,child)
            handle[parent][child][0].click()
        except Exception as e:
            logger.debug('Exception Found %s Trying to click directly Child %s',e,child)
            handle[child][0].click()

        # handle['cm'][Constants.CONTEXTMENU][0].click()
        # self.handle.
    def drillTo(self,driver,driverHelper,handles,pageName):
        try:
            logger.debug('Launching Page %s',pageName)
            if pageName == Constants.NETWORKFUNCTIONS:
                handles[Constants.DRILLTONF][0].click()
            elif pageName == Constants.SITEINTERACTIONS:
                handles[Constants.DRILLTOSITEINTERACTION][0].click()
            elif pageName == Constants.SITES:
                handles[Constants.DRILLTOSITE][0].click()
            elif pageName == Constants.VRF:
                handles[Constants.DRILLTOVRF][0].click()
            elif pageName==Constants.NETWORKELEMENTS:
                handles[Constants.DRILLTONE][0].click()
            elif pageName == Constants.DRILLTO:
                handles[Constants.DRILLTO][0].click()
            elif pageName == Constants.NENE:
                handles[Constants.DRILLTONENE][0].click()
            elif pageName == Constants.EXPORTTO:
                handles[Constants.EXPORTTO][0].click()
            elif pageName == Constants.EXPORTTOCSV:
                handles[Constants.EXPORTTOCSV][0].click()
            elif pageName == Constants.EXPORTTOSNAPSHOT:
                handles[Constants.EXPORTTOSNAPSHOT][0].click()
            return True
        except Exception as e:
            logger.debug('Exception Found %s while Launching Page %s',e,pageName)
            return e


    def launchTrends(self,handle):
        try:
            handle['cm']['trends'][0].click()
            return True
        except Exception:
            return Exception.message

    def GenerateReports(self,handle):
        handle['cm']['generatereport'][0].click()






    # def activateContextMenuOptions(self,handlers):
    #     handle = self.compHandlers('cm',handlers)
    #     handle["CONTEXTMENU"][len(handle["CONTEXTMENU"])-1].click()
    #     # self.handle.

    def getDrillToOptions(self,handlers):
        handle = self.compHandlers('cm',handlers)
        #Opens DrillToOptions
        handle['DRILLTO'][len(handle["DRILLTO"])-1].click()

        # handle['DRILLTO'][len(handle["DRILLTO"])-1].find_elements_by_xpath(".//*")
        return [ele.text for ele in handle['DRILLTO'][len(handle["DRILLTO"])-1].find_elements_by_tag_name("label")]

        # handle['DRILLTO'][len(handle["DRILLTO"])-1].find_elements_by_tag_name("label")



    # def drillTo(self,driver,driverHelper,handles,pageName):
    #     handle = self.compHandlers('cm',handles)
    #
    #     # Open Drillto options
    #     handle["CONTEXTMENU"][len(handle["CONTEXTMENU"])-1].click()
    #
    #     children = handle[Constants.CONTEXTMENU][len(handle[Constants.CONTEXTMENU])-1].find_elements_by_xpath(".//*")
    #
    #     handle[pageName][len(handle[pageName]) -1].click()


    # def selectTrends(self,driver,driverHelper,handles,pageName):
    #     pass
    #     # handles['trends']


    def activate(self,h,parent='exploreBar',child='cm'):
        try:
            logger.info("Going to click Context Menu Option")
            h[parent][child][0].click()
            logger.info("Context Menu Option Clicked")
            return True
        except Exception as e:
            logger.error("Got Exception while clicking Context Menu = %s",str(e))
            raise e

    def goto(self,value,h,parent='exploreBar',child='a'):
        try:
            for e in h[parent][child]:
                if value == str(e.text):
                    logger.info("Going to click Option = %s",e.text)
                    e.click()
                    return True
            logger.debug("No option with %s present to be clicked",str(value))
        except Exception as e:
            logger.error("Got Exception while clicking Option %s = %s",value,str(e))
            return e


    def gotoScreenViaBreadCrumb(self,screenName,h,parent="breadcrumb",child='bar'):
        for e in h[parent][child]:
            if str(e.text) == screenName:
                e.click()
                break

    def gotoScreenViaWorkFlowDrop(self,screenName,h,parent="breadcrumb",child='workflow'):
        for e in h[parent][child][0].find_elements_by_xpath(".//*"):
            if str(e.text).strip().strip('\n').strip() == screenName:
                e.click()
                break

    def activateWorkFlowDropDown(self,h,parent="breadcrumb",child='workflow'):
        try:
            h[parent][child][0].click()
            return True
        except Exception as e:
            logger.error("Got Exception while launching WorkFlow Dropdown = %s",str(e))
            return e

    def getScreenName(self,h,parent="exploreBar",child='labels'):
        try:
            screenName =  str(h[parent][child][0].text)
            logger.info("Got Screen Name = %s",screenName)
            return screenName
        except Exception as e:
            logger.error("Got Exception while getting Screen Name = %s",str(e))
            return e

    def getRHSBreadCrumbLabel(self,h,parent="exploreBar",child='labels'):
        try:
            screenName =  str(h[parent][child][1].text)
            logger.info("Got BreadCrumb Label = %s",screenName)
            return screenName
        except Exception as e:
            logger.error("Got Exception while getting Breadcrumb Label = %s",str(e))
            return e
