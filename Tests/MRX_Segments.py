import unittest
from Utils.logger import *

from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *


class Test001(unittest.TestCase):


    def setUp(self):
        sleep(5)
        logger.info('**************Test MRX_SEGMENT started**************')
        self.driver = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver54')
        # self.driver = webdriver.Firefox()
        self.driver.get("http://192.168.113.147:3000/")
        self.driverHelper = DriverHelper(self.driver)


    def test_site(self):
        # Login to Page
        # login(self.driver,self.driverHelper,Constants.USERNAME,Constants.PASSWORD)
        # Launch Sites Page
        mrxSegmentScreen(self.driver,self.driverHelper,"segment_Screen")
        # drilltoScreen(self.driver,self.driverHelper,Constants.NETWORKFUNCTIONS)



    def tearDown(self):
        self.driver.close()
        logger.info('**************Test MRX_SEGMENT completed**************')

if __name__ == "__main__":
    unittest.main(exit=False)
