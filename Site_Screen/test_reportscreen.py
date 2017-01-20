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
reportScreenHandle = getHandle(setup,"report_Screen","table")
downloadcompleted = reportScreenInstance.dropdown.click(reportScreenHandle['table']['download1'][1])
reportScreenInstance.dropdown.click(reportScreenHandle['table']['delete1'][1])
reportScreenHandle = getHandle(setup,"report_Screen")
deletecompleted = reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['ok'])
reportScreenHandle = getHandle(setup,"report_Screen")
swticher = reportScreenInstance.switcher.switchTo(1,reportScreenHandle,'createdialog','switcher')
reportScreenHandle = getHandle(setup,"report_Screen")
reportScreenInstance.dropdown.click(reportScreenHandle['table']['delete1'][1])
reportScreenHandle = getHandle(setup,"report_Screen")
deletepending = reportScreenInstance.dropdown.customClick(reportScreenHandle['report']['ok'])
checkEqualAssert(downloadcompleted,True,"","","Download button Completed Tab Validation")
checkEqualAssert(deletecompleted,True,"","","Delete button completed Tab Validation")
checkEqualAssert(deletepending,True,"","","Delete button pending Tab Validation")
setup.d.close()