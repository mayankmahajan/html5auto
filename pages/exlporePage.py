from locators import ExplorePageLocators
from selenium import webdriver

from practice.page import waitFor


class ExploreElements:
    '''Login Page'''

    ''' Use Firefox'''
    # driver=webdriver.Firefox()

    ''' Class Constructor '''
    def __init__(self,driver=webdriver):
        '''
        :param driver: instance for webDriver Firefox
        :return:
        '''

    def get_site_element(self):
        waitFor(self,ExplorePageLocators.SITES)
        return self.driver.find_element(ExplorePageLocators.SITES)


