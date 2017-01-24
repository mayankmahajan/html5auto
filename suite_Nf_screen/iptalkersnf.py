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
nfScreenInstance.cm.GenerateReports(nfScreenHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report_popup")


filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
# grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
grPopInstance.dropdown.doSelection(grPopHandle,"Top IP Talker Report","generateReportDialog","reportType")
# grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],"TopIP")
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


checkEqualAssert(result,"sitereports","","","Network Function Report is verified")


# Closing the Testcase
setup.d.close()
