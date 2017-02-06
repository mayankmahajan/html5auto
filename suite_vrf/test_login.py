import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *

# Getting Setup Details and Launching the application
setup = SetUp()


# Getting TimeRange Info from Config Files
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
print measureIteration
measures = setup.cM.getNodeElements("measures","measure").keys()
print measures
# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)
# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Get the default selection
#defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
#checkEqualAssert(str(1),str(defSelection['selIndex']),"NA","NA","")

# Set the bar Table view to the 2 index
a = screenInstance.btv.setSelection(2,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.VRF)


#siteScreenHandle = getHandle(setup,"vrf_Screen")


#measures testing
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        result = setMeasure(setup,measures[i],"vrf_Screen")



         # Result Logging


        checkEqualAssert(result,True,"Checking the measuers at Vrf Screen "+"Time:-"+ quicklinks[t], "Measuers :- "+measures[i])
        i+=1
         # end of measureSelection


    t+=1
     # end of while loop for QuicklinkSelections
