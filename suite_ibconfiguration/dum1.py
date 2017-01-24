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
from classes.Pages.ConfigurationPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")

setup.d.switch_to.window(setup.d.window_handles[1])
confScreenInstance = ConfigurationPageClass(setup.d)
confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
confScreenInstance.searchComp.setSearchText(confScreenHandle,"3.3.3.3")
confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
confScreenHandle = getHandle(setup,"configuration_Screen")

confScreenInstance.table.setSelection1(1,confScreenHandle,"table")
confScreenHandle = getHandle(setup,"configuration_Screen","buttons")
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][1])
setup.d.switch_to_alert().accept()
confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.dummyelement.doSelection(confScreenHandle,"Site",'searchSelector','select')
confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
confScreenInstance.searchComp.setSearchText(confScreenHandle,"3.3.3.3")
confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
confScreenHandle = getHandle(setup,"configuration_Screen","table")
data = confScreenInstance.table.getTableData1(confScreenHandle,"table")

search = validatesearchtable(data,"IP","3.3.3.3")
checkEqualAssert(search,False,"IP","Site IB Configuration","Delete Validation")



setup.d.close()