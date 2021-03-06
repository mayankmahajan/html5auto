import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.InterfacePageClass import *
from classes.Pages.GenerateReportsPopClass import *



# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","interface_Screen")
# Get the Instance of the screen
screenInstance = InterfacePageClass(setup.d)

# Get the handles of the screen
interfaceScreenHandle = getHandle(setup,Constants.INTERFACES)

# Export to csv
exportTo(setup,setup.dH,'EXPORTTOSNAPSHOT')
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup")
result = grPopInstance.reportspopup.clickButton("Download",grPopHandle)
# Result logging
checkEqualAssert(result,True,"","","EXPORT TO SNAPSHOT Validated at Interface Screen")

#Closing the application
setup.d.close()