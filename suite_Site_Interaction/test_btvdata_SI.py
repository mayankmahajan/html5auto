import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from Utils.csvReader import *
from classes.Pages.SiteIntScreenClass import *

data = {}
# Getting Setup Details and Launching the application
setup = SetUp()

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

# Checking drill to the Site Interaction Screen
result = drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

# Get the Instance of the screen
sitescreenInstance = SiteIntScreenClass(setup.d)

# Get the handles of the screen
siteintScreenHandle = getHandle(setup,"siteInteraction_Screen")

btvData = sitescreenInstance.btv.getData(siteintScreenHandle)
# btvData = screenInstance.btv.getData(siteScreenHandle)
data['btvData'] = {}
for key,value in btvData.iteritems():
    pv = value.pop(0)
    if len(data['btvData']) == 0:
        data['btvData']['dimension'] = value
    else:
        data['btvData']['value'] = value
    logger.debug('Col1 : %s  and Col2 : %s',key,value)

csvreader = CSVReader()

result = sitescreenInstance.btv.validateBTVData(data,csvreader.csvData)
print result
# for key,value in result.iteritems():
#      logger.debug('DIMENSION : %s  and RESULT : %s',key,value)

# Logging out of the application
setup.d.close()
