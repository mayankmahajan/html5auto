import unittest
from Utils.logger import *

from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *


class Test2(unittest.TestCase):


    def setUp(self):
        logger.info('**************Test2 started**************')
        self.driver = webdriver.Firefox()
        self.driver.get(Constants.URL)
        self.driverHelper = DriverHelper(self.driver)


    def test_sites(self):
        '''
        Test2 : Validate Data present at BTV
        login : Logins to App
        launchPage : Launch Page (say Sites)
        getBTVData : Get Bar Tabular View Data
        '''
        login(self.driver,self.driverHelper,Constants.USERNAME,Constants.PASSWORD)
        launchPage(self.driver,self.driverHelper,Constants.SITES)
        data = getBTVData(self.driver,self.driverHelper)


    def tearDown(self):
        self.driver.close()
        logger.info('**************Test2 completed**************')

if __name__ == "__main__":
    unittest.main(exit=False)
