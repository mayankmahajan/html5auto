from scripts.locators import LoginPageLocators,ExplorePageLocators,SitePageLocators
from selenium import webdriver

from practice.page import waitFor
from practice.page import waitForVisible


class BaseElements:
    def __init__(self,driver=webdriver):
        pass

''' Login Page Elements'''
class LoginElements(BaseElements):
    '''Login Page'''

    # ''' Use Firefox'''
    # driver=webdriver.Firefox()


    def get_userName_element(self,driver):
        waitForVisible(driver,LoginPageLocators.USERNAME)
        return driver.find_element(*LoginPageLocators.USERNAME)

    def get_password_element(self,driver):
        waitForVisible(driver,LoginPageLocators.PASSWORD)
        return driver.find_element(*LoginPageLocators.PASSWORD)

    def get_signIn_element(self,driver):
        waitForVisible(driver,LoginPageLocators.SIGNIN)
        return driver.find_element(*LoginPageLocators.SIGNIN)


''' Explore Page Elements'''
class ExploreElements(LoginElements):
    '''Explore Page'''

    def get_page_element(self,page):
        if page in ExplorePageLocators:
            pass
            # locator = ExplorePageLocators
    def get_site_element(self,driver):
        waitForVisible(driver,ExplorePageLocators.SITES)
        return driver.find_element(*ExplorePageLocators.SITES)

''' Site Page Elements'''
class SiteElements(ExploreElements):
    '''Site Page'''

    def get_btv(self,driver):
        waitForVisible(driver,SitePageLocators.BTV)
        return driver.find_element(*SitePageLocators.BTV)

    def get_right_selection_label(self,driver):
        waitForVisible(driver,SitePageLocators.RIGHTSELECTIONLABEL)
        return driver.find_element(*SitePageLocators.RIGHTSELECTIONLABEL)



