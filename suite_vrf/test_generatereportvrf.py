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
reportname = "Vrf_report"
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

vrfscreenHandle = getHandle(setup,Constants.VRF,"cm")
vrfscreenInstance.cm.activateContextMenuOptions1(vrfscreenHandle)
vrfscreenHandle = getHandle(setup,Constants.VRF,"cm")
vrfscreenInstance.cm.GenerateReports(vrfscreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],reportname)
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"deepanshu.ahuja@guavus.com")
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["generate"])
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["close"])
date = currentdate()
grPopHandle = getHandle(setup,"report_popup")
grPopInstance.dropdown.customClick(grPopHandle['successdialog']["ok"])

exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
reportScreenInstance = ReportsModuleClass(setup.d)
reportScreenHandle = getHandle(setup,"report_Screen")

reportScreenInstance.switcher.switchTo(1,reportScreenHandle,'createdialog','switcher')
# reportScreenHandle = getHandle(setup,"report_Screen")

data = reportScreenInstance.table.getTableData1(getHandle(setup,"report_Screen"),"table")
# result = data['rows'][0][1]
# type = data['rows'][0][2]
# reportid = IsreportIDvalid(data)
# uidate = data['rows'][0][5]
if (data['rows'][0][1] == reportname):
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Validating the VRF Report name")
    checkEqualAssert(data['rows'][0][2],"Site Report Average","Today","","Validating the VRF Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Validating VRF Report ID")
    checkEqualAssert(data['rows'][0][5],date,"Today","","Checking the Requested time of the Vrf report")
else:
    reportScreenHandle = getHandle(setup,"report_Screen")
    reportScreenInstance.switcher.switchTo(0,reportScreenHandle,'createdialog','switcher')
    reportScreenHandle = getHandle(setup,"report_Screen")
    data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Validating the VRF Report name")
    checkEqualAssert(data['rows'][0][2],"Site-VRF Report Average","Today","","Validating the VRF Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Validating VRF Report ID")
    checkEqualAssert(data['rows'][0][4],date,"Today","","Checking the Requested time of the Vrf report")
# Closing the Testcase
setup.d.close()