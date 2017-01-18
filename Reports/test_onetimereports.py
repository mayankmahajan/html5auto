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
grPopHandle = getHandle(setup,"report2_popup")
grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
grPopHandle = getHandle(setup,"report2_popup")
