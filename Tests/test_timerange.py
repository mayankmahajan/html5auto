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


exploreScreenInstance.exploreList.switchApp(exploreHandle,2)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])




forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")

forensicsScreenInstance.dummyelement.customClick(forensicsScreenHandle['commoncomponents']['newquery'])

popupInstance = GenerateReportsPopClass(setup.d)
popupHandler = getHandle(setup,"routers_popup")

dateSelected = popupInstance.routerpopup.setTime(0,popupHandler,'queryrouters','wizard1',setup,"07-11-2016-03-00")

# dateSelected = popupInstance.

queryName = popupInstance.routerpopup.setQueryName("query1",popupHandler,'queryrouters','wizard1')
sortBy = popupInstance.routerpopup.setSortBy("PROTOCOL",popupHandler,'queryrouters','wizard1')
sortOrder = popupInstance.routerpopup.setSortOrder("ASC",popupHandler,'queryrouters','wizard1')
pageSize = popupInstance.routerpopup.setPageSize("500",popupHandler,'queryrouters','wizard1')

data = popupInstance.routertable.getTableData1(popupHandler,'routertable')
popupInstance.routertable.setSelection1(2,popupHandler,'routertable')










# Closing the Testcase
setup.d.close()