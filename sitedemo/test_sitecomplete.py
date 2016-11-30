import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.QuickTrendsPageClass import QuickTrendsPageClass




######################## COMPLETE SITE SCREEN #########################

# Getting Setup Details and launching the application
setup = SetUp()

# Logging into the setup
result = login(setup, "admin", "Admin@123")

#Checking the login functionality
checkEqualAssert("True",str(result),"TODAY","","LOGIN SUCCESSFULL")

# Launch Site Screen
status = launchPage(setup,"site_Screen")

# Checking the launch page of the site page
checkEqualAssert(status,True,"","","SITE PAGE LAUNCHES SUCCESSFULLY")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"","","DEFAULT SELECTION IS CORRECT")

# Set the bar Table view to the 1 index
screenInstance.btv.setSelection(2,siteScreenHandle)
btvSelection = screenInstance.btv.getSelection(siteScreenHandle)

#Validate Summary Bar Data
# summaryBarData = getSummaryBarData("Bitrate_total_absolute_peak",btvSelection['BTVCOLUMN1'],screenInstance,siteScreenHandle)
# message = "Data validated with summary bar " + str(btvSelection['BTVCOLUMN2']) + " "
# checkEqualAssert(btvSelection['BTVCOLUMN2'],summaryBarData,"<quicklink>","Bitrate_total_absolute_peak",message)


# Get Bar Tabular Data and Tooltip
btvData = screenInstance.btv.getData(siteScreenHandle)
data = {}
data['btvData'] = parseBTVData(btvData)
data['btvTooltipData'] = screenInstance.btv.getToolTipInfo(setup.d,setup.dH,siteScreenHandle)
checkEqualAssert(screenInstance.btv.validateToolTipData1(data),True,"TODAY","Bitrate_total_absolute_peak","ToolTipdata")

#Change TimeRange
setTimeRange(setup,"YESTERDAY")

#Do Search
screenInstance.searchComp.setSearchText(siteScreenHandle,"ATL")
screenInstance.searchComp.hitSearchIcon(siteScreenHandle)

siteScreenHandle = getHandle(setup,"site_Screen")
# screenInstance.btv.setSelection(2,siteScreenHandle)
#
# screenInstance.cm.activateContextMenuOptions(siteScreenHandle)
# screenInstance.cm.launchTrends(siteScreenHandle)
#
# qtScreenInstance = QuickTrendsPageClass(setup.d)
# qtScreenHandle = getHandle(setup,"qt_Screen")
#
# list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
#
# singlesitename = btvSelection['BTVCOLUMN1']
# list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
# legendname = list[0]
#
# checkEqualAssert(singlesitename,legendname,"TODAY","","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")




# xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
# yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)
#
# print qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)

# DataValidation for Trends will be done from Backend








