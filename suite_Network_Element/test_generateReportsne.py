import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.NEPageClass import *
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

reportname = "nereport"
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Checking the drill to
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)

#######################################################################
#Create screen instance and get handle of screen
neScreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
#######################################################################

neScreenInstance.pielegend.setSelection1(setup.dH,[0],neScreenHandle,'pielegend')

# exportTo(setup.d,setup.dH,Constants.EXPORTTOCSV)

########################################################################
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
neScreenInstance.cm.activateContextMenuOptions1(neScreenHandle)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS,"cm")
neScreenInstance.cm.GenerateReports(neScreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],reportname)
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"mayank.mahajan@guavus.com")
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["generate"])
date = currentdate()
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["close"])
#
grPopHandle = getHandle(setup,"report_popup")
grPopInstance.dropdown.customClick(grPopHandle['successdialog']["ok"])


exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")

reportScreenInstance = ReportsModuleClass(setup.d)
reportScreenHandle = getHandle(setup,"report_Screen")

reportScreenInstance.switcher.switchTo(1,reportScreenHandle,'createdialog','switcher')
reportScreenHandle = getHandle(setup,"report_Screen")

data = reportScreenInstance.table.getTableData1(getHandle(setup,"report_Screen"),"table")
# result = data['rows'][0][1]
# type = data['rows'][0][2]
# reportid = IsreportIDvalid(data)
# uidate = data['rows'][0][5]
if (data['rows'][0][1] == reportname):
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Checking the Network Element Report name")
    checkEqualAssert(data['rows'][0][2],"Site-Network Element Report Average","Today","","Checking the Network Element Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Checking the Network Element Report ID")
    checkEqualAssert(data['rows'][0][5],date,"Today","","Checking the Requested time for Network Element Report")
else:
    reportScreenHandle = getHandle(setup,"report_Screen")
    reportScreenInstance.switcher.switchTo(0,reportScreenHandle,'createdialog','switcher')
    reportScreenHandle = getHandle(setup,"report_Screen")
    data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
    checkEqualAssert(data['rows'][0][1],reportname,"Today","","Checking the Network Element Report name")
    checkEqualAssert(data['rows'][0][2],"Site-Network Element Report Average","Today","","Checking the Network Element Report Type")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Checking the Network Element Report ID ")
    checkEqualAssert(data['rows'][0][4],date,"Today","","Checking the Requested Time for Network Element Report")
# Closing the Testcase
setup.d.close()

