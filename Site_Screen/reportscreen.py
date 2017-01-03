from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *


# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
reportScreenInstance = ReportsModuleClass(setup.d)
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.dropdown.click(reportScreenHandle['table']['download'][1])
reportScreenInstance.dropdown.click(reportScreenHandle['table']['delete'][1])
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['ok'])
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.switcher.switchTo(1,reportScreenHandle,'createdialog','switcher')
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.dropdown.click(reportScreenHandle['table']['delete'][1])
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['ok'])
setup.d.close()