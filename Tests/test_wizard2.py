import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.ForensicsPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")
setup.d.switch_to.window(setup.d.window_handles[1])

# Getting Handle
popupInstance = GenerateReportsPopClass(setup.d)
popupHandler = getHandle(setup,"routers_popup")

# popupInstance.reportspopup.clickButton("Next Step",popupHandler)
popupInstance.routerpopup.add("addrule",popupHandler)
popupInstance.routerpopup.updateGroup("rule",["DST PORT","in",2],popupHandler)
# Closing the Testcase
setup.d.close()