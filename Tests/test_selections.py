import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *


# Getting Setup Details
setup = SetUp()

# Getting TimeRange Info
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))

# Getting Measures Info
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()


# Launching Application
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,"site_Screen")

# while loop is to iterate over all the quicklinks
while (timeIteration > 0):
    i=0
    setTimeRange(setup,timeIteration)

    # while loop is to iterate over all the measure
    while i < measureIteration:
        setMeasure(setup,measures[i],"site_Screen")

        # testcase body starts









        # testcase body ends

        # Result Logging
        checkEqualAssert("mayank",setup.d.current_url,__name__)
        i+=1
        # end of measureSelection


    timeIteration-=1
    # end of while loop for QuicklinkSelections


# Closing the Testcase
setup.d.close()