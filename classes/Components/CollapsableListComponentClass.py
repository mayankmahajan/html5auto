#!/usr/bin/env python
##############################################################
'''
BarTabular Component Handler
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
from Utils.logger import *

from selenium.webdriver import ActionChains



class CollapsableListComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

    def getSelectedRowHandle(self,h,parent="leftListContainer",child="selected"):
        logger.info("Fetching Selected Row Info for Collapsable List")
        try:
            return h[parent][child][0]
        except Exception as e:
            raise e

    def getSelectedRow(self,h,parent="leftListContainer",child="selected",occurence=0):
        logger.info("Fetching Selected Row Info for Collapsable List")
        data = {}
        selArr = h[parent][child][occurence].text.strip().strip("\n").strip().split("\n")
        data['dim'] = str(selArr[0])
        data['value'] = str(selArr[1])
        try:
            return data
        except Exception as e:
            raise e
    def setIndex(self,setup,h,index=0,parent="leftListContainer",child="draggables"):
        logger.info("Going to select Row : "+str(index)+" at Collapsable List" )
        try:
            if not h['leftListContainer']['draggables']:
                self.takeScreenshot(setup.d)
                logger.debug("No DATA on Collapsable List")
                raise
                return Constants.NODATA
            h['leftListContainer']['draggables'][index].click()
            return True
        except Exception as e:
            raise
    def getData(self,setup,h,parent="leftListContainer",child="draggables"):
        logger.info("Going to get all Rows from Collapsable List")
        drags = h['leftListContainer']['draggables']
        try:
            if not drags:
                self.takeScreenshot(setup.d)
                logger.debug("No DATA on Collapsable List")
                raise
            return [e.text for e in drags]
        except Exception as e:
            raise e

