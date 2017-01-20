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
wizardIteration = len(setup.cM.getNodeElements("wizardquicklinks","wizardquicklink"))
quicklinks = setup.cM.getNodeElements("wizardquicklinks","wizardquicklink").keys()
reportname = "timereports"
reports = []
login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# Reports Module
###################################
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
for i in range(wizardIteration):

    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenHandle = getHandle(setup,"report_Screen")

    reportScreenInstance.launchCreateReport(setup.d)
    grPopInstance = GenerateReportsPopClass(setup.d)
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.reportspopup.selectRadioButton("Average",grPopHandle)
    grPopInstance.reportspopup.selectRadioButton("Network Function Report",grPopHandle)
    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.reportspopup.selectRadioButton(quicklinks[i],grPopHandle)
    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportnamewizard"],reportname)
    grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInputwizard"],"deepanshu.ahuja@guavus.com")
    grPopInstance.reportspopup.clickButton("Submit",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    result = grPopInstance.dropdown.customClick(grPopHandle['successdialog']['ok'])

    checkEqualAssert(result,True,quicklinks[i],"","Validation")

setup.d.close()

