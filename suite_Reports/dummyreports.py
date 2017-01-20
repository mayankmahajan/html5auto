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
# Getting Measures Info from Config Files
siteIteration = len(setup.cM.getNodeElements("sitetypes","sitetype"))
sites = setup.cM.getNodeElements("sitetypes","sitetype").keys()
ar = []
n = [1]
reportname = "site"
login(setup, "admin", "Admin@123")
# exploreScreenInstance = ExplorePageClass(setup.d)
# exploreHandle = getHandle(setup,"explore_Screen")
#
# # suite_Reports Module
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
############################### time reports ###########################
# grPopHandle = getHandle(setup,"report2_popup")
# grPopInstance.reportspopup.selectRadioButton("Today",grPopHandle)
# grPopHandle = getHandle(setup,"report2_popup")
# starttime = getInputText(grPopHandle,'generateReportDialog','starttime')
# endtime = getInputText(grPopHandle,'generateReportDialog','endtime')
# grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
############################## time reports completed ####################

######################### get table data ######################################
for j in range(0,2):
    grPopHandle = getHandle(setup,"report2_popup")

    # grPopInstance.table.getTableCells(grPopHandle)
    # ar.append(grPopInstance.table.selectTableCellIndex(1,grPopHandle))
    # b = grPopInstance.table.selectTableCellIndex(1,grPopHandle) + "("+sites[0]+")"
    ar.append(grPopInstance.table.selectTableCellIndex(1,grPopHandle))
    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
###############################get table data completed########################
print ar
grPopHandle = getHandle(setup,"report2_popup")
# grPopHandle['generateReportDialog'][0].text
print grPopHandle['generateReportDialog']['filters'][0].text
a = FindWordInString(ar,grPopHandle)
print a
# starttimeend =getInputText(grPopHandle,'generateReportDialog','starttime')
# endtimeend = getInputText(grPopHandle,'generateReportDialog','endtime')
# checkEqualAssert(starttime,starttimeend,"","","Start Time validation")
# checkEqualAssert(endtime,endtimeend,"","","End Time validation")
setup.d.close()
