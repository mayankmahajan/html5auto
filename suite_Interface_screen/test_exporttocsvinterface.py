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



# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","interface_Screen")
# Get the Instance of the screen
screenInstance = InterfacePageClass(setup.d)

# Get the handles of the screen
interfaceScreenHandle = getHandle(setup,Constants.INTERFACES)

result = exportTo(setup,setup.dH,'EXPORTTOCSV')

checkEqualAssert(result,True,"","","EXPORT TO CSV IS COMPLETED SUCCESSFULL AT INTERFACE SCREEN")

setup.d.close()