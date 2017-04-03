from classes.DriverHelpers.DriverHelper import *
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import *



class SetUp:
    def __init__(self):

        security = True

        if security:
            if "chrome" == Constants.BROWSER:
                chromeOptions = webdriver.ChromeOptions()
                # chromeOptions.add_argument("--kiosk")
                chromeOptions.add_argument("--start-maximized")

                # self.d = webdriver.Firefox()
                self.d = webdriver.Chrome(Constants.chromedriverpath, chrome_options=chromeOptions)
            elif "ff" == Constants.BROWSER:
                self.d = webdriver.Firefox()
            elif "safari" == Constants.BROWSER:
                self.d = webdriver.Safari()



            # self.d = webdriver.Chrome(Constants.chromedriverpath)
        else:

            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--disable-web-security")
            chromeOptions.add_argument("--user-data-dir")
            self.d = webdriver.Chrome(Constants.chromedriverpath,chrome_options=chromeOptions)


        # firefox_capabilities = DesiredCapabilities.FIREFOX
        # firefox_capabilities['marionette'] = True
        # firefox_capabilities['binary'] = '/Users/mayank.mahajan/node_modules/geckodriver/geckodriver'
        #
        #
        # executable_path ='/Users/mayank.mahajan/node_modules/geckodriver/geckodriver'
        # binary = FirefoxBinary('/Applications/Firefox.app')
        # self.d = webdriver.Firefox(capabilities=firefox_capabilities,firefox_binary=binary,executable_path=executable_path)


        # self.d = webdriver.Firefox()
        self.d.get(Constants.URL)
        self.d.maximize_window()
        self.dH = DriverHelper(self.d)
        self.cM = ConfigManager()

