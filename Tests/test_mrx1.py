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
from selenium.webdriver import ActionChains
from classes.Pages.UDPageClass import *



setup = SetUp()

login(setup, "admin", "Admin@123")
# exploreScreenInstance = ExplorePageClass(setup.d)
# exploreHandle = getHandle(setup,"explore_Screen")
#
# # UD Module
# ####################################
# exploreScreenInstance.exploreList.launchModule(exploreHandle,"USER DISTRIBUTION")
screenInstance = UDPageClass(setup.d)
screenHandle = getHandle(setup,"ud_Screen")
screenInstance.table.setSpecialSelection(setup.d,[2,4],Keys.SHIFT,screenHandle)


s=screenHandle['body']['startdrag'][0]
e=screenHandle['body']['enddrag'][0]

ActionChains(setup.d).drag_and_drop(s,e).perform()
ActionChains(setup.d).click_and_hold(s).move_by_offset(200,0).perform()

grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"udp_popup")


grPopInstance.clickLink("",grPopHandle)
grPopInstance.getAllSelectedFilters(grPopHandle)


grPopInstance.multiDropdown.domultipleSelection(grPopHandle,"Netbook",0)


# Closing the Testcase
setup.d.close()