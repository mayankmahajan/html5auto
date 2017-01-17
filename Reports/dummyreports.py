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
from Utils.utility import *
import random

setup = SetUp()

# login(setup, "cmathieu", "a")

ar = []
n = [1]
reportname = "site"
login(setup, "admin", "Admin@123")
# exploreScreenInstance = ExplorePageClass(setup.d)
# exploreHandle = getHandle(setup,"explore_Screen")
#
# # Reports Module
# ###################################
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
# reportScreenInstance = ReportsModuleClass(setup.d)
# reportScreenHandle = getHandle(setup,"report_Screen")
#
# reportScreenInstance.launchCreateReport(setup.d)
grPopInstance = GenerateReportsPopClass(setup.d)
# grPopHandle = getHandle(setup,"report2_popup")
# grPopInstance.reportspopup.selectRadioButton("Average",grPopHandle)
# grPopInstance.reportspopup.selectRadioButton("Site Report",grPopHandle)
#
# grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
# grPopHandle = getHandle(setup,"report2_popup")
# grPopInstance.reportspopup.selectRadioButton("Today",grPopHandle)
# grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
#
#
#
# grPopHandle = getHandle(setup,"report2_popup")
# grPopInstance.table.getTableCells(grPopHandle)
#
# ar.append(grPopInstance.table.selectTableCellIndex(1,grPopHandle))
# grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)

grPopHandle = getHandle(setup,"report2_popup")
a = getInputText(grPopHandle,'generateReportDialog','starttime')
b = getInputText(grPopHandle,'generateReportDialog','endtime')
print a
print b
setup.d.close()
