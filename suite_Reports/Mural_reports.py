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
# exploreScreenInstance = ExplorePageClass(setup.d)
# exploreHandle = getHandle(setup,"explore_Screen","appHeader")
#
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")

reports = ["Gateway Traffic"]
for i in range(len(reports)):

    # reportScreenInstance = ReportsModuleClass(setup.d)
    #
    # reportScreenInstance.launchCreateReport1(setup.d)
    grPopInstance = GenerateReportsPopClass(setup.d)
    # grPopHandle = getHandle(setup,"report2_popup","radios")
    # grPopInstance.reportspopup.selectRadioButton(reports[i],grPopHandle,"label")
    # grPopHandle = getHandle(setup, "report2_popup", "allbuttons")
    # grPopInstance.reportspopup.clickButton("Next Step", grPopHandle)
    grPopHandle = getHandle(setup, "report2_popup", "generateReportDialog")

    # starttime = getHandle(setup,'generateReportDialog','starttime1')
    grPopHandle['generateReportDialog']['starttime1'][0].click()
    setCalendar("2016", "Aug", "10", "00", "00", grPopInstance, setup,"report2_popup")
    grPopInstance.reportspopup.clickButton("Apply", grPopHandle)
    endtime = getInputText(grPopHandle,'generateReportDialog','endtime1')

    # grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
