import unittest
from Utils.logger import *

from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *

class Test6(unittest.TestCase):

    # def __init__(self):
    #     self.setup = SetUp()


    # def setUp(self):
    #     sleep(5)
    #     logger.info('**************Test6 started**************')
        # self.driver = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver')
        # self.driver = webdriver.Firefox()
        # self.driver.get(Constants.URL)
        # self.driver.get("https://nrmca-upgrade-setup.sprintspectrum.com:6443/")
        # self.driverHelper = DriverHelper(self.driver)



    def test_site(self):
        setup = SetUp()
        # Login to Page

        login(setup,Constants.USERNAME,Constants.PASSWORD)
        testScreen(setup,"site_Screen",True)
        drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)
        # Launch Sites Page
        testScreen(setup,"siteInteraction_Screen")
        # drilltoScreen(self.driver,self.driverHelper,Constants.NETWORKFUNCTIONS)



    # def tearDown(self):
    #     self.driver.close()
    #     logger.info('**************Test6 completed**************')

if __name__ == "__main__":
    unittest.main(exit=False)
