#!/usr/bin/env python
##############################################################
'''
Quick Trends Component Handler
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
from selenium.common.exceptions import *

from selenium.webdriver import ActionChains



class GenerateReportsComponentClass(BaseComponentClass):
    def __init__(self):
        BaseComponentClass.__init__(self)


    # def selectRadioButton(self,value,h,parent="radios",child="radio"):
    #     for el in h[parent][child]:
    #         if value == el.find_elements_by_xpath("..//span")[0].text:
    #             try:
    #                 el.click()
    #             except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
    #                 return e
    #
    # def clickButton(self,value,h,parent="allbuttons",child="button"):
    #     for el in h[parent][child]:
    #         if value == el.text:
    #             try:
    #                 el.click()
    #             except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
    #                 return e




