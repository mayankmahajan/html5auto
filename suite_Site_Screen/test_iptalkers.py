import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *


# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")


# Launch Site Screen
# launchPage(setup,"site_Screen")

reportname = "Topip"
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

siteScreenHandle = getHandle(setup,"site_Screen")
screenInstance.cm.activateContextMenuOptions1(siteScreenHandle)
screenInstance.cm.GenerateReports(siteScreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
# grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Top IP Talker Report","generateReportDialog","reportType")
# grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
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
reportScreenHandle = getHandle(setup,"report_Screen")

data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")

if (data['rows'][0][1] == reportname):
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Top IP Report name")
    checkEqualAssert(data['rows'][0][2],"Site Report Average","Today","","Top IP Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","The Top IP Report ID")
    checkEqualAssert(data['rows'][0][5],date,"Today","","Time of the top ip report")
else:
    reportScreenHandle = getHandle(setup,"report_Screen")
    reportScreenInstance.switcher.switchTo(0,reportScreenHandle,'createdialog','switcher')
    reportScreenHandle = getHandle(setup,"report_Screen")
    data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Top IP Report name")
    checkEqualAssert(data['rows'][0][2],"Top IP Talker Report","Today","","Top IP Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","The Top IP Report ID")
    checkEqualAssert(data['rows'][0][4],date,"Today","","Time of the top ip report")
# Closing the Testcase
setup.d.close()