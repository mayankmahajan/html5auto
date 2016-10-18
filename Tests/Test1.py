import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *


class Test1(unittest.TestCase):


    def setUp(self):
        sleep(5)
        logger.info('**************Test1 started**************')
        # setupTestcase(self)
        self.driver = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver')
        # self.driver = webdriver.Firefox()
        self.driver.get(Constants.URL)
        self.driverHelper = DriverHelper(self.driver)

    def test_login(self):
        login(self.driver,self.driverHelper,Constants.USERNAME,Constants.PASSWORD)

    def tearDown(self):
        self.driver.close()
        logger.info('**************Test1 completed**************')



if __name__ == "__main__":
    unittest.main(exit=False)
