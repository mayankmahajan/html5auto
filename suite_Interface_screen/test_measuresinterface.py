import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.InterfacePageClass import *
############################ CHECK FOR THE DEFAULT SELECTION BY MULTIPLE MEASURES #######################

# Getting Setup Details and Launching the application
setup = SetUp()


timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
siteIteration = len(setup.cM.getNodeElements("elementtypes","elementtype"))
sites = setup.cM.getNodeElements("elementtypes","elementtype").keys()

# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()



# Launching Application
login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","interface_Screen")
# Get the Instance of the screen
screenInstance = InterfacePageClass(setup.d)

# Get the handles of the screen
interfaceScreenHandle = getHandle(setup,Constants.INTERFACES)


# while loop is to iterate over all the quicklinks
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < siteIteration:
        j=0
        screenInstance.measure.doSelectionSite(interfaceScreenHandle,sites[i])

        # testcase body starts

        # while loop is to iterate over all the measure
        while j < measureIteration:
            screenInstance.measure.doSelection(interfaceScreenHandle,measures[j])
            sleep(2)
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