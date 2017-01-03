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

login(setup, "admin", "Admin@123")
# exploreScreenInstance = ExplorePageClass(setup.d)
# exploreHandle = getHandle(setup,"explore_Screen")
#
# # UD Module
# ####################################
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"USER DISTRIBUTION")
setup.d.execute_script("document.getElementsByClassName('createReportBtn')[0].click()")
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"udp_popup")

grPopInstance.multiDropdown.domultipleSelection(grPopHandle,"Netbook",0)


# Closing the Testcase
setup.d.close()