from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from classes.DriverHelpers.CustomWebDriverWait import CustomWebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.Constants import *

class DriverHelper:
    def __init__(self,driver):
        self.driver = driver

    # def

    def waitForVisibleElement(self, locator):
        # self.driver = driver
        CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def waitForVisibleElements(self, locator):
        # self.driver = driver
        CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
        return self.driver.find_elements(*locator)

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
            print(element,locator)
            CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
            dict_element_handlers[element] = self.driver.find_elements(*locator)
        return dict_element_handlers


