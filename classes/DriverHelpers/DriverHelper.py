#!/usr/bin/env python
##############################################################
'''
Driver Helper Class
supplies Webdriver controller
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from classes.DriverHelpers.CustomWebDriverWait import CustomWebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.Constants import *
from selenium.webdriver import ActionChains
from Utils.ConfigManager import ConfigManager
import time


class DriverHelper:
    def __init__(self,driver):
        self.driver = driver
        # self.action = webdriver.ActionChains(driver)
        self.action = ActionChains(driver)
        self.configManager = ConfigManager()
        # self.sleep = time.sleep(2)
        # hover = self.action.move_to_element_with_offset()
        # hover.perform()
        # webdriver.Firefox.find_element_by_xpath()


    # def

    def waitForVisibleElement(self, locator, wait=True, isParent = False):
        # self.driver = driver
        if wait:
            CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def waitForVisibleElements(self, locator, wait=True, parentHandles = {}, comp = '', locatorDimension = '', locatorText = '', parentDependency = 'True'):
        # self.driver = driver
        # if wait == True:
        tempChildHandles = []
        if parentHandles != {} and parentDependency == 'True':
            for eachComp in parentHandles.keys():
                if comp in self.configManager.componentChildRelations[eachComp]:
                    if wait:
                        print comp,locator
                        CustomWebDriverWait(parentHandles[eachComp][0], Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))

                    if locatorDimension != '':
                        # tempChilds = []
                        for eachChild in parentHandles[eachComp][0].find_elements('xpath','.//*'):
                            try:
                                if locatorText in eachChild.get_attribute(locatorDimension):
                                    tempChildHandles.append(eachChild)
                            except:
                                pass
                    else:
                        tempChildHandles = tempChildHandles +  self.driver.find_elements(*locator)
                else:
                    if wait:
                        CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
                    tempChildHandles = tempChildHandles + self.driver.find_elements(*locator)
        else:
            if wait:
                CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
            tempChildHandles = tempChildHandles +  self.driver.find_elements(*locator)

        return tempChildHandles



    def waitForVisibleElementsAndChild(self, element_locator_pairs):
        # self.driver = driver
        dict_element_handlers = {}
        for element,locator in element_locator_pairs.iteritems():
            CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
            dict_element_handlers[element] = self.driver.find_element(*locator)
        return dict_element_handlers

    def waitForVisibleElementsAndChilds(self, element_locator_pairs):
        # self.driver = driver
        dict_element_handlers = {}
        for element,locator in element_locator_pairs.iteritems():
            print(element,locator)  # parentHandles['btv'][0].find_elements('xpath','.//*')[2].get_attribute('class')
            CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
            dict_element_handlers[element] = self.driver.find_elements(*locator)
        return dict_element_handlers

# webdriver.Firefox().find_element_by_tag_name().find_element_by_xpath('//*[contains(@class, "column0")]').
