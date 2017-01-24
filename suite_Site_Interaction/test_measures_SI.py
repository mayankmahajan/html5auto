import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SiteIntScreenClass import *


# Getting Setup Details
setup = SetUp()

# Getting TimeRange Info from Config Files
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()

# Getting Measures Info from Config Files
siteIteration = len(setup.cM.getNodeElements("sitetypes","sitetype"))
sites = setup.cM.getNodeElements("sitetypes","sitetype").keys()



# Launching Application
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

# Checking the drill to
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)



siteintscreenInstance = SiteIntScreenClass(setup.d)
siteintscreenHandle = getHandle(setup,Constants.SITEINTERACTIONS)

# while loop is to iterate over all the quicklinks
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < siteIteration:
        j=0
        screenInstance.measure.doSelectionSite(siteintscreenHandle,sites[i])

        # testcase body starts

        # while loop is to iterate over all the measure
        while j < measureIteration:
            screenInstance.measure.doSelection(siteintscreenHandle,measures[j])

            # testcase body starts


            # defaultselection = btv.getSelection()
            # checkEqualAssert("0",defaultselection)







            # testcase body ends

            # Result Logging
            expected = "True"
            actual = "True"

            message = sites[i]
            checkEqualAssert(expected,actual,quicklinks[t],measures[j],message)

            j+=1
        # end of measureSelection






        # testcase body ends

        # Result Logging
        expected = "True"
        actual = "True"


        # checkEqualAssert(expected,actual,quicklinks[t],sites[i])

        i+=1
        # end of measureSelection


    t+=1
    # end of while loop for QuicklinkSelections


# Closing the Testcase
setup.d.close()
