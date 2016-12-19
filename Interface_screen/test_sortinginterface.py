import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.InterfacePageClass import *



# Getting Setup Details
setup = SetUp()


# Launching Application
login(setup, "admin", "Admin@123")


# launchPage(setup,"site_Screen")
# siteScreenInstance = SitePageClass(setup.d)
# siteScreenHandle = getHandle(setup,"site_Screen")
#
# data = siteScreenInstance.btv.getData(siteScreenHandle)

# Launch Screen
launchPage(setup,Constants.INTERFACES)

# Get the Instance of the screen
screenInstance = InterfacePageClass(setup.d)

# Get the handles of the screen
interfaceScreenHandle = getHandle(setup,Constants.INTERFACES)

interfacedata = screenInstance.table.getIterfaceTableData(interfaceScreenHandle)

setup.d.close()
