import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.VrfPageClass import *
from classes.Components.SearchComponentClass import *
#from Utils.HelperUtility import *
# Getting Setup Details and Launching the application
setup = SetUp()

# Getting TimeRange Info from Config Files
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()


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

# Drill to the Site Interaction Screen

drilltoScreen(setup.d,setup.dH,Constants.VRF)
screenInstance = VrfPageClass(setup.d)
VRFScreenHandle = getHandle(setup, Constants.VRF)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        print i
        screenInstance.measure.doSelection(VRFScreenHandle, measures[i])

        # testcase body starts
        # Get the Instance of the screen
        VRFScreenHandle = getHandle(setup, Constants.VRF)
        #validate=HelperUtility()
        result=screenInstance.validate.ValidateSummarybar(VRFScreenHandle, measures[i], "btv", screenInstance, setup,Constants.VRF)
        checkEqualAssert(result[0], result[1], quicklinks[t], measures[i], result[2])
        i+=1
    t+=1


setup.d.close()