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
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")


exploreScreenInstance.exploreList.switchApp(exploreHandle)
result = exploreScreenInstance.exploreList.launchapp(getHandle(setup,"explore_Screen"),2)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])

forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")

download = forensicsScreenInstance.dropdown.click(forensicsScreenHandle['netflowtable']['download'][1])
forensicsScreenInstance.dropdown.click(forensicsScreenHandle['netflowtable']['delete'][1])
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup","allbuttons")
delete = grPopInstance.reportspopup.clickButton("Ok",grPopHandle)
checkEqualAssert(download,True,"","","Download button validation")
checkEqualAssert(delete,True,"",""," Delete button validation")

setup.d.close()
