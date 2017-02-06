import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.QuickTrendsPageClass import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.ConfigurationPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","nf_Screen")
exploreScreenInstance.exploreList.switchApp(exploreHandle)
result = exploreScreenInstance.exploreList.launchapp(getHandle(setup,"explore_Screen"),1)

setup.d.switch_to.window(setup.d.window_handles[1])
checkEqualAssert(result,True,"","","Launch IB Configuration Validation")

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
