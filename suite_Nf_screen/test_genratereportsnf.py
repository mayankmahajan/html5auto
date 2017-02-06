import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.QuickTrendsPageClass import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *

setup = SetUp()

# login(setup, "cmathieu", "a")

reportname = "nfreport"

login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","nf_Screen")


# exploreScreenInstance.exploreList.switchApp(exploreHandle,1)

# suite_Reports Module
####################################
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
# reportScreenInstance = ReportsModuleClass(setup.d)
# reportScreenHandle = getHandle(setup,"report_Screen")
# reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['create'])




# launchPage(setup,"nf_Screen")
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,"nf_Screen")
# nfScreenInstance.pielegend.setSelection(setup.dH,[2],nfScreenHandle)
nfScreenInstance.pielegend.setSelection1(setup.dH,[1],nfScreenHandle,'pielegend')

# exportTo(setup.d,setup.dH,Constants.EXPORTTOCSV)

########################################################################
nfScreenHandle = getHandle(setup,"nf_Screen")
nfScreenInstance.cm.activateContextMenuOptions1(nfScreenHandle)
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS,"cm")
nfScreenInstance.cm.GenerateReports(nfScreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],reportname)
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"mayank.mahajan@guavus.com")
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

data = reportScreenInstance.table.getTableData1(getHandle(setup,"report_Screen"),"table")
# result = data['rows'][0][1]
# type = data['rows'][0][2]
# reportid = IsreportIDvalid(data)
# uidate = data['rows'][0][5]
if (data['rows'][0][1] == reportname):
    checkEqualAssert(data['rows'][0][1],reportname,"Time :- Today","","Checking the name of the Network Function Report")
    checkEqualAssert(data['rows'][0][2],"Network Function Report Average","Time :- Today","","Checking the Type of the Network Function Report")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Checking the Report ID of the Network Function Report")
    checkEqualAssert(data['rows'][0][5],date,"Today","","Checking the Requested Time of the Network Function Report")
else:
    reportScreenHandle = getHandle(setup,"report_Screen")
    reportScreenInstance.switcher.switchTo(0,reportScreenHandle,'createdialog','switcher')
    reportScreenHandle = getHandle(setup,"report_Screen")
    data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
    checkEqualAssert(data['rows'][0][1],reportname,"Time :- Today","","Checking the name of the Network Function Report")
    checkEqualAssert(data['rows'][0][2],"Network Function Report Average","Today","","Checking the Type of the Network Function Report")
    checkEqualAssert(IsreportIDvalid(data),True,"","","Checking the Report ID of the Network Function Report")
    checkEqualAssert(data['rows'][0][4],date,"Time :-Today","","Checking the Requested Time of the Network Function Report")
# Closing the Testcase
setup.d.close()