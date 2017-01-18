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
queryname = "query2"
login(setup, "admin", "Admin@123")

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])

popupInstance = GenerateReportsPopClass(setup.d)
popupHandler = getHandle(setup,"routers_popup")
popupInstance.calendar.set("minute","02",popupHandler)


setup.d.close()