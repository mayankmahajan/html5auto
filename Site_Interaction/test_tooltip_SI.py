import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.BTVComponentClass import *



data = {}
# Getting Setup Details and Launching the application
setup = SetUp()

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

# Checking drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)


# Get the Instance of the screen
sitescreenInstance = SitePageClass(setup.d)
siteintScreenHandle = getHandle(setup,"siteInteraction_Screen")
# screenInstance.measure.doSelectionSite(siteScreenHandle,"SatSite")


#setMeasure(setup,"Bitrate_total_absolute_average","site_Screen")

# Get the handles of the screen
# siteScreenHandle = getHandle(setup,"site_Screen")

btvData = sitescreenInstance.btv.getData(siteintScreenHandle)
data['btvData'] = {}
for key,value in btvData.iteritems():
    pv = value.pop(0)
    if len(data['btvData']) == 0:
        data['btvData']['dimension'] = value
    else:
        data['btvData']['value'] = value
    logger.debug('Col1 : %s  and Col2 : %s',key,value)
data['btvTooltipData'] = sitescreenInstance.btv.getToolTipInfo(setup.d,setup.dH,siteintScreenHandle)
sleep(2)
checkEqualAssert(True,True,"TODAY","Bitrate_total_absolute_peak","TOOLTIP IS WORKIG PERFECTLY")
print data['btvTooltipData']
result1 = sitescreenInstance.btv.validateToolTipData1(data)
print result1

checkEqualAssert(result1,True,"TODAY","Bitrate_total_absolute_peak","ToolTipdata")
setup.d.close()