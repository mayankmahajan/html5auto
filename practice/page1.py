from selenium.webdriver.support.wait import WebDriverWait

from element import BasePageElement
from scripts.locators import ExplorePageLocators
from scripts.locators import LoginPageLocators
from variables import LoginPageVariables


def waitFor(self,locator):
    WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*locator))

class LoginPageElement(BasePageElement):
    locator = 'q'


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):

    def is_title_matches(self):
        """Verifies that the hardcoded text "Python" appears in page title"""
        return "NR-MCA" in self.driver.title


    # __username = ''
    # def __getattr__(self, __username):
    #     return __username
    # def __setattr__(self, __username, value):
    #     __username = value
    #     return __username
    # username = LoginPageElement(*LoginPageLocators.USERNAME)

    def send_username(self):

        element = self.driver.find_element(*LoginPageLocators.USERNAME)
        element.send_keys(LoginPageVariables.USERNAME)

    def send_password(self):
        element = self.driver.find_element(*LoginPageLocators.PASSWORD)
        element.send_keys(LoginPageVariables.PASSWORD)

    def click_signIn(self):
        element = self.driver.find_element(*LoginPageLocators.SIGNIN)
        element.click()


class ExplorePage(BasePage):

    def is_Site_Available(self):
        # WebDriverWait(self.driver, 100).until(
        #     lambda driver: driver.find_element(*ExplorePageLocators.SITES))
        waitFor(self,*ExplorePageLocators.SITES)
        return "Sites" in self.driver.find_element(*ExplorePageLocators.SITES).text