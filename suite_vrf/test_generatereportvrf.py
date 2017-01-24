import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.VrfPageClass import *


# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")


# Launch Site Screen
# launchPage(setup,"site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Checking the drill to
drilltoScreen(setup.d,setup.dH,Constants.VRF)

vrfscreenInstance = VrfPageClass(setup.d)
vrfscreenHandle = getHandle(setup, Constants.VRF)

# Set the Index value at 2
vrfscreenInstance.btv.setSelection(2,vrfscreenHandle)

vrfscreenHandle = getHandle(setup,Constants.SITEINTERACTIONS)
vrfscreenInstance.cm.activateContextMenuOptions1(vrfscreenHandle)
vrfscreenInstance.cm.GenerateReports(vrfscreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],"siteinteractionreport")
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"deepanshu.ahuja@guavus.com")
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["generate"])
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["close"])

# grPopHandle = getHandle(setup,"report_popup")
# grPopInstance.dropdown.customClick(grPopHandle['successdialog']["ok"])
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
reportScreenInstance = ReportsModuleClass(setup.d)
reportScreenHandle = getHandle(setup,"report_Screen")
data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
result = data['rows'][0][1]
# print data['header']
# print data['rows']
# print data['rows']['00']
# print data['rows']['00'][0]
# print data['rows'][0]
# print data['rows'][1]
# print data['rows'][2]
print data['rows'][0][1]
checkEqualAssert(result,"sitereports","","","VRF Report is verified")

# Closing the Testcase
setup.d.close()