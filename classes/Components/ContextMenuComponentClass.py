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
class ContextMenuComponentClass(BaseComponentClass):

    def activateContextMenuOptions(self,handle):
        handle[Constants.CONTEXTMENU][0].click()
        # self.handle.
    def drillTo(self,driver,driverHelper,handles,pageName):
        try:
            if pageName == Constants.NETWORKFUNCTIONS:
                handles[Constants.DRILLTONF][0].click()
            elif pageName == Constants.SITEINTERACTIONS:
                handles[Constants.DRILLTOSITEINTERACTION][0].click()
            elif pageName == Constants.SITES:
                handles[Constants.DRILLTOSITE][0].click()
            elif pageName == Constants.VRF:
                handles[Constants.DRILLTOVRF][0].click()
            elif pageName == Constants.DRILLTO:
                handles[Constants.DRILLTO][0].click()
            return True
        except Exception:
            return Exception


    def launchTrends(self,handle):
        handle['trends'][0].click()






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

