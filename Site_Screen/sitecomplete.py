import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *



######################## COMPLETE SITE SCREEN #########################

# Getting Setup Details and launching the application
setup = SetUp()

timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
siteIteration = len(setup.cM.getNodeElements("sitetypes","sitetype"))
sites = setup.cM.getNodeElements("sitetypes","sitetype").keys()

# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()

# Logging into the setup
result = login(setup, "admin", "Admin@123")

#Checking the login functionality
checkEqualAssert("True",str(result),"TODAY","","LOGIN SUCCESSFULL")

# Launch Site Screen
launchPage(setup,"site_Screen")

# Checking the launch page of the site page
checkEqualAssert(True,True,"","","SITE PAGE LAUNCHES SUCCESSFULLY")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"","","DEFAULT SELECTION IS CORRECT")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(3,siteScreenHandle)


#Changing the measure
a = setMeasure(setup,"Bitrate_downlink_absolute_average","site_Screen")

# Get the new handles of the screen
handles = getHandle(setup,Constants.SITES) # Everytime we need to get handles when the btv is redrawing

# Get the selection after changing the measures
changeselection =  screenInstance.btv.getSelection(handles)


# Validating the result after changing the measure
checkEqualAssert(str(1),str(changeselection['selIndex']),"TODAY","Bitrate_downlink_absolute_average","DEFAULT SELECTION IS CORRECT ")

