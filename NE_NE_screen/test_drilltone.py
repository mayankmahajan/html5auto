import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

screen_name='site_Screen'
# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,screen_name)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,screen_name)


# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"NA","NA","to check def selection should be one")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
#Drill to NE screen
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)


# Get the instance of the ne screen
neScreenInstance= NEPageClass(setup.d)

#get the handle of ne screen
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

#select any pielagent on ne screen
neScreenInstance.pielegend.setSelection(setup.dH,[3],neScreenHandle)

#Drill to nene screen
drilltoScreen(setup.d,setup.dH,Constants.NENE)