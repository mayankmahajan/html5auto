import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Components.SearchComponentClass import *
from Utils.HelperUtility import *

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

# Launch Site Screen
launchPage(setup,"site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Drill to the Site Interaction Screen

drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)
screenInstance = NEPageClass(setup.d)
NEScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        screenInstance.measure.doSelection(NEScreenHandle, measures[i])

        # testcase body starts
        # Get the Instance of the screen
        NEScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)
        result=ValidateSummarybar(NEScreenHandle,measures[i],"pielegend",screenInstance,setup,Constants.NETWORKELEMENTS)
        print result
        checkEqualAssert(result[0], result[1], quicklinks[t], measures[i], result[2])
        i+=1
    t+=1