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

# login(setup, "cmathieu", "a")


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
# grPopInstance = GenerateReportsPopClass(setup.d)
# grPopHandle = getHandle(setup,"report2_popup")
# grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup")
# dateSelected = grPopInstance.routerpopup.setTime2(0,grPopHandle,'reportwizard','starttime',setup,"24-03-2016-03-00")
# grPopInstance.routerpopup.doCalendarSelection(setup,'reportwizard',0,"24-03-2016-03-00")
grPopInstance.dropdown.customClick(grPopHandle['reportwizard']['starttime'])
grPopHandle = getHandle(setup,"report2_popup")
grPopInstance.routerpopup.doCalendarSelection(setup,)
setup.d.close()