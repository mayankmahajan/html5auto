import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SwitcherComponentClass import *
# Getting Setup Details and Launching the application

setup = SetUp()
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
print quicklinks
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
print measureIteration
measures = setup.cM.getNodeElements("measures","measure").keys()
print measures



# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen

launchPage(setup,"site_Screen")
sleep(5)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

#set timerange and measure
# setTimeRange(setup,"TODAY")
# setMeasure(setup,"Flows_uplink_percentage_average","site_Screen")
# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

test_case1="Default selection of site screen"
# Get the default selection
# defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
# checkEqualAssert(str(1),str(defSelection['selIndex']),"Today","Flows",test_case1)

# Set the bar Table view to the 2 index
a = screenInstance.btv.setSelection(2,siteScreenHandle)

siteScreenHandle = getHandle(setup, "site_Screen")
#btvdata=screenInstance.btv.getData(siteScreenHandle)
#print btvdata
print screenInstance.btv.getToolTipInfo(setup.d, setup.dH,siteScreenHandle)

drilltoScreen(setup.d,setup.dH,Constants.VRF)

vrfscreeinstance = SitePageClass(setup.d)
vrfScreenHandle = getHandle(setup,Constants.VRF)
#btvdata=screenInstance.btv.getData(vrfScreenHandle)
#print btvdata
print screenInstance.btv.getToolTipInfo(setup.d, setup.dH,vrfScreenHandle)