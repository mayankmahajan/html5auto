from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DriverHelper:
    def __init__(self,driver):
        self.driver = driver

    def waitForVisibleElement(self, locator):
        # self.driver = driver
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def waitForVisibleElements(self, locator):
        # self.driver = driver
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def waitForVisibleElementsAndChilds(self, locator, child):
        # self.driver = driver
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located(locator))
        return self.driver.find_elements(*locator)


