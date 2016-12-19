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
# exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","nf_Screen")


exploreScreenInstance.exploreList.switchApp(exploreHandle,1)

# Reports Module
####################################
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
# reportScreenInstance = ReportsModuleClass(setup.d)
# reportScreenHandle = getHandle(setup,"report_Screen")
# reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['create'])




# launchPage(setup,"nf_Screen")
# nfScreenInstance = NFPageClass(setup.d)
# nfScreenHandle = getHandle(setup,"nf_Screen")

# exportTo(setup.d,setup.dH,Constants.EXPORTTOCSV)

########################################################################

# nfScreenInstance.cm.activateContextMenuOptions(nfScreenHandle)
# nfScreenInstance.cm.GenerateReports(nfScreenHandle)
#
# grPopInstance = GenerateReportsPopClass(setup.d)
# grPopHandle = getHandle(setup,"report_popup")
#
#
# filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
# grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
# grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
# grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],"report1")
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
# grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"mayank.mahajan@guavus.com")
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["generate"])
# grPopHandle = getHandle(setup,"report_popup")
# grPopInstance.dropdown.customClick(grPopHandle['successdialog']["ok"])


# Closing the Testcase
setup.d.close()