from classes.DriverHelpers.DriverHelper import *


class SetUp:
    def __init__(self):
        self.d = webdriver.Chrome('/Users/vivek.aggarwal/Downloads/chromedriver')
        self.d.get(Constants.URL)
        self.dH = DriverHelper(self.d)
        self.cM = ConfigManager()

