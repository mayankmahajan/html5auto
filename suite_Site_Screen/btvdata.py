import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from Utils.csvReader import *


#### NOT RUNNING DUE TO BUG

# Getting Setup Details and Launching the application
setup = SetUp()
data = {}
# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,"site_Screen")
sleep(5)
#logger.debug("btv_data_btsdfsdsdfsfsffsfs")
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# data = getBTVData(setup.d,setup.dH)
btvData = screenInstance.btv.getData(siteScreenHandle)
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

result = screenInstance.btv.validateBTVData(data,csvreader.csvData)
print result
# for key,value in result.iteritems():
#      logger.debug('DIMENSION : %s  and RESULT : %s',key,value)

# Logging out of the application
setup.d.close()