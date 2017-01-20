import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SiteIntScreenClass import *
# Getting Setup Details and Launching the application
setup = SetUp()

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

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Checking drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

# Get the Instance of the screen
sitescreenInstance = SiteIntScreenClass(setup.d)

# Get the handles of the screen
siteintScreenHandle = getHandle(setup,Constants.SITEINTERACTIONS)

# Set the bar Table view to the 2 index
sitescreenInstance.btv.setSelection(2,siteintScreenHandle)

result = exportTo(setup,setup.dH,'EXPORTTOCSV')

checkEqualAssert(result,True,"","","EXPORT TO CSV IS COMPLETED SUCCESSFULL AT SITE INTERACTION")

setup.d.close()


