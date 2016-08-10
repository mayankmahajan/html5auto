import unittest
from Utils.logger import *

from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *


class Test7(unittest.TestCase):


    def setUp(self):
        logger.info('**************Test7 started**************')
        self.driver = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver')
        # self.driver = webdriver.Firefox()
        self.driver.get(Constants.URL)
        self.driverHelper = DriverHelper(self.driver)


    def test_site(self):
        # Login to Page
        login(self.driver,self.driverHelper,Constants.USERNAME,Constants.PASSWORD)
        testScreen1(self.driver,self.driverHelper,"site_Screen",True)
        drilltoScreen(self.driver,self.driverHelper,Constants.SITEINTERACTIONS)
        # Launch Sites Page
        testScreen1(self.driver,self.driverHelper,"siteInteraction_Screen")
        drilltoScreen(self.driver,self.driverHelper,Constants.VRF)
        testScreen1(self.driver,self.driverHelper,"vrf_Screen")



    def tearDown(self):
        self.driver.close()
        logger.info('**************Test7 completed**************')

if __name__ == "__main__":
    unittest.main(exit=False)
