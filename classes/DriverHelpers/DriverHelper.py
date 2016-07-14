from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from classes.DriverHelpers.CustomWebDriverWait import CustomWebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.Constants import *
from selenium.webdriver import ActionChains
import time



# class Actions:
#     def __init__(self,driver):
#         self.driver = driver



class DriverHelper:
    def __init__(self,driver):
        self.driver = driver
        # self.action = webdriver.ActionChains(driver)
        self.action = ActionChains(driver)
        # self.sleep = time.sleep(2)
        # hover = self.action.move_to_element_with_offset()
        # hover.perform()
        # webdriver.Firefox.find_element_by_xpath()


    # def

    def waitForVisibleElement(self, locator):
        # self.driver = driver
        CustomWebDriverWait(self.driver, Constants.WEBDRIVERTIMEOUT).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def waitForVisibleElements(self, locator, wait=True):
        # self.driver = driver
        if wait:
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

# webdriver.Firefox().find_element_by_tag_name().find_element_by_xpath('//*[contains(@class, "column0")]').
