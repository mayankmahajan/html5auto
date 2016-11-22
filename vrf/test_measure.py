import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.VRFpage import  *
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

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,"site_Screen")


# Get the default selection
#defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
#checkEqualAssert(str(1),str(defSelection['selIndex']),"","")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.VRF)

vrfscreeinstancen = VRFpage(setup.d)
vrfScreenHandle = getHandle(setup,Constants.VRF)


# while loop is to iterate over all the quicklinks
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        status = screenInstance.measure.doSelection(vrfScreenHandle, measures[i])
        setMeasure(setup,measures[i],Constants.VRF)
        checkEqualAssert("True", str(status), quicklinks[t], measures[i], "Measure selection")
        i+=1
         # end of measureSelection

    t+=1

     # end of while loop for QuicklinkSelections


# Logging out the application
setup.d.close()
#checkEqualAssert("True",result,"","","drillToNF")