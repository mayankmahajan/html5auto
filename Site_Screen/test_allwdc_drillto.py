import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *


################################ CHECKING ALL WDC DRILL TO OPTION #####################

#### NOT RUNNING DUE TO BUG
# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# CHECKING THE DRILL TO FUNCTION FOR THE ALL WDC
drill = drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

checkEqualAssert(True,drill,"TODAY","","ALL WDC DRILLTO HAS TO BE FAILED")

# LOGGINGING OUT THE APPLICATION
setup.d.close()
