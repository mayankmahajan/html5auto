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
import random

setup = SetUp()
login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# Reports Module
###################################
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
reportScreenInstance = ReportsModuleClass(setup.d)
reportScreenHandle = getHandle(setup,"report_Screen")

reportScreenInstance.launchCreateReport(setup.d)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup","radios")
grPopInstance.reportspopup.selectRadioButton("Average",grPopHandle)
grPopInstance.reportspopup.selectRadioButton("Network Function Report",grPopHandle)
grPopHandle = getHandle(setup,"report2_popup","allbuttons")
grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)

grPopHandle = getHandle(setup,"report2_popup","radios")

grPopInstance.reportspopup.selectRadioButton("Recurring report",grPopHandle)

grPopHandle = getHandle(setup,"report2_popup","allimages")
grPopHandle['allimages']['image'][4].click()
setCalendar("2016","March","24","02","00",grPopInstance,setup)
grPopHandle = getHandle(setup,"report2_popup","allbuttons")
grPopInstance.reportspopup.clickButton("Apply",grPopHandle)
grPopHandle = getHandle(setup,"report2_popup","recurring")
grPopInstance.dropdown.doSelection(grPopHandle,"Daily","recurring","dropdowns")
grPopHandle = getHandle(setup,"report2_popup","recurring")
grPopInstance.dropdown.customSendkeys(grPopHandle['recurring']["instances"],"1")

grPopHandle = getHandle(setup,"report2_popup","allbuttons")
grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)

grPopHandle = getHandle(setup,"report2_popup")
grPopInstance.table.selectTableCellIndex(1,grPopHandle)
grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)


grPopHandle = getHandle(setup,"report2_popup","generateReportDialog")
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportnamewizard"],"wizard1")
grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInputwizard"],"deepanshu.ahuja@guavus.com")
grPopHandle = getHandle(setup,"report2_popup","allbuttons")
grPopInstance.reportspopup.clickButton("Submit",grPopHandle)
grPopHandle = getHandle(setup,"report2_popup","allbuttons")
result = grPopInstance.reportspopup.clickButton("OK",grPopHandle)

checkEqualAssert(result,True,"","","Recurring Report Validation")



setup.d.close()