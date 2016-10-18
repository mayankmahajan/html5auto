import unittest
from Utils.logger import *

from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *


class Test3(unittest.TestCase):


    def setUp(self):
        sleep(5)
        logger.info('**************Test3 started**************')
        self.driver = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver')
        # self.driver = webdriver.Firefox()
        self.driver.get(Constants.URL)
        self.driverHelper = DriverHelper(self.driver)


    def test_nf(self):
        # Login to Page
        login(self.driver,self.driverHelper,Constants.USERNAME,Constants.PASSWORD)
        # Launch Sites Page
        launchPage(self.driver,self.driverHelper,Constants.SITES)
        # Gets Data from BTV
        data = getBTVData(self.driver,self.driverHelper)
        drilltoScreen(self.driver,self.driverHelper,Constants.NETWORKFUNCTIONS)


    def tearDown(self):
        self.driver.close()
        logger.info('**************Test3 completed**************')

if __name__ == "__main__":
    unittest.main(exit=False)
