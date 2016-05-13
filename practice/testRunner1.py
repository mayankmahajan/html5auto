from pages.commonPage import LoginElements,ExploreElements,SiteElements
# from pages.exlporePage import ExploreElements
from selenium import webdriver
import unittest


def login():
    '''
    :return: Logins to App
    '''

    loginElements.get_userName_element().send_keys('admin')
    loginElements.get_password_element().send_keys('Admin@123')
    loginElements.get_signIn_element().click()

def goto_sites():
    exploreElements.get_site_element().click()

class TestRunner(unittest.TestCase):

    def test_01_verifyTitle(self):
        self.assertEqual('Sites',exploreElements.get_site_element().text,'Text not matched')

    def test_02_verifyTitle1(self):
        self.assertEqual('Sites',exploreElements.get_site_element().text,'Text not matched')

    def test_03_SelectionLabel(self):
        goto_sites()
        if (siteElements.get_btv().is_displayed()):
            self.assertEqual('XYZ',siteElements.get_right_selection_label(),'Label not correct')

    @classmethod
    def tearDownClass(cls):
        loginElements.driver.close()

if __name__ == '__main__':
    loginElements = LoginElements(webdriver)
    exploreElements = ExploreElements(webdriver)
    siteElements = SiteElements(webdriver)
    loginElements.driver.get("https://nrmca.guavus.com:6443/")
    loginElements.driver.maximize_window()
    login()
