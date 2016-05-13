from selenium.webdriver.support.ui import WebDriverWait

from scripts.locators import LoginPageLocators


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(self.locator))
        driver.find_element(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(self.locator))
        element = driver.find_element(self.locator)
        return element.get_attribute("value")

    # def __set__(self, obj, value):
    #     """Sets the text to the value supplied"""
    #     driver = obj.driver
    #     WebDriverWait(driver, 100).until(
    #         lambda driver: driver.find_element_by_name(self.locator))
    #     driver.find_element_by_name(self.locator).send_keys(value)
    #
    # def __get__(self, obj, owner):
    #     """Gets the text of the specified object"""
    #     driver = obj.driver
    #     WebDriverWait(driver, 100).until(
    #         lambda driver: driver.find_element_by_name(self.locator))
    #     element = driver.find_element_by_name(self.locator)
    #     return element.get_attribute("value")







class LoginPageElement(BasePageElement):



    # def __init__(self):
    #     self.__userName = "";

    __userName = ""
    __userName_locator = LoginPageLocators.USERNAME
    def getUserName(self):
        return self.__userName
    def setUserName(self, userName):
        self.__userName = userName



