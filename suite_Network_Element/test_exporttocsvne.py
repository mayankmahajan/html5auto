import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *

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
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)

nescreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

result = exportTo(setup,setup.dH,'EXPORTTOCSV')

checkEqualAssert(result,True,"","","EXPORT TO CSV IS COMPLETED SUCCESSFULL AT NETWORK ELEMENT SCREEN")

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()

