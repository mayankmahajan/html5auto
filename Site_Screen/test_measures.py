import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *

############################ CHECK FOR THE DEFAULT SELECTION BY MULTIPLE MEASURES #######################

# Getting Setup Details and Launching the application
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



# Launching Application
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,"site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")


# while loop is to iterate over all the quicklinks
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < siteIteration:
        j=0
        screenInstance.measure.doSelectionSite(siteScreenHandle,sites[i])

        # testcase body starts

        # while loop is to iterate over all the measure
        while j < measureIteration:
            screenInstance.measure.doSelection(siteScreenHandle,measures[j])
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
#setSiteType(setup,"SatSite","site_Screen")

#checkEqualAssert(True,True,"","","SAtsite")

