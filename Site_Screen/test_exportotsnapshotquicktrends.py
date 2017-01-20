import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.QuickTrendsPageClass import *




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

screenInstance.cm.activateContextMenuOptions1(siteScreenHandle)

screenInstance.cm.launchTrends(getHandle(setup,"site_Screen","cm"))

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

# Export to csv
exportTo(setup,setup.dH,'EXPORTTOSNAPSHOT')
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup")
result = grPopInstance.reportspopup.clickButton("Download",grPopHandle)
# Result logging
checkEqualAssert(result,True,"","","EXPORT TO SNAPSHOT quick trends")

#Closing the application
setup.d.close()