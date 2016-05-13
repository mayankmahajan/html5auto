from pages.commonPage import LoginElements,ExploreElements,SiteElements
# from pages.exlporePage import ExploreElements
from selenium import webdriver
from scripts.Constants import Constants
import unittest
from scripts.logger import logger
from scripts.logintoApp import LoginApp
from scripts.exploreApp import ExploreApp

def goto_sites(self):
    self.exploreElements.get_site_element().click()

class TestCase1(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     pass
    # def __init__(self,x):
    #     self.driver = webdriver.Firefox()
    #     loginApp = LoginApp(self.driver)
    #     loginApp.login(self.driver)
    #     logger.info('Login Successful 1')
    #     self.exploreElements = ExploreElements(self.driver)
    #     self.siteElements = SiteElements(self.driver)
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        loginApp = LoginApp(self.driver)
        loginApp.login(self.driver)
        logger.info('Login Successful 1')
        self.exploreElements = ExploreElements(self.driver)
        self.siteElements = SiteElements(self.driver)

    def test_01_verifyTitle(self):
        self.assertEqual('Sites',self.exploreElements.get_site_element().text,'Text not matched')
        logger.debug('%s',self.exploreElements.get_site_element().text)

    def test_02_verifyTitle1(self):
        self.assertEqual('Sites',self.exploreElements.get_site_element().text,'Text not matched')
        logger.debug('%s',self.exploreElements.get_site_element().text)

    def test_03_SelectionLabel(self):
        exploreApp = ExploreApp(self.driver)
        exploreApp.gotoPage(self.driver,'Sites')
        # goto_sites(self)
        self.exploreElements.get_site_element(self.driver)
        self.siteElements.get_btv()
        self.assertEqual('ANAHEIMCAWDC',self.siteElements.get_right_selection_label().text,'Label not correct')
        logger.debug('%s',self.siteElements.get_right_selection_label().text)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
