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

dateSelected = popupInstance.routerpopup.setTime(0,popupHandler,'queryrouters','wizard1',setup,"24-03-2016-03-00")
# popupHandler = getHandle(setup,"routers_popup")
dateSelected = popupInstance.routerpopup.setTime(1,popupHandler,'queryrouters','wizard1',setup,"12-11-2016-03-00")


# dateSelected = popupInstance.

queryName = popupInstance.routerpopup.setQueryName(queryname,popupHandler,'queryrouters','wizard1')
sortBy = popupInstance.routerpopup.setSortBy("PROTOCOL",popupHandler,'queryrouters','wizard1')
sortOrder = popupInstance.routerpopup.setSortOrder("ASC",popupHandler,'queryrouters','wizard1')
pageSize = popupInstance.routerpopup.setPageSize("500",popupHandler,'queryrouters','wizard1')


data = popupInstance.routertable.getTableData1(popupHandler,'routertable')
popupInstance.routertable.setSelection1(2,popupHandler,'routertable')
popupHandler = getHandle(setup,"routers_popup")
popupInstance.reportspopup.clickButton("Next Step",popupHandler)
popupHandler = getHandle(setup,"routers_popup")
popupInstance.reportspopup.clickButton("Submit Query",popupHandler)
date = currentdate()
popupHandler = getHandle(setup,"routers_popup")
popupInstance.reportspopup.clickButton("Ok",popupHandler)
forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")
forensicsScreenInstance.switcher.switchTo(1,forensicsScreenHandle,'createdialog','switcher')

data = forensicsScreenInstance.table.getTableData1(getHandle(setup,"report_Screen"),"netflowtable")
# result = data['rows'][0][1]
# type = data['rows'][0][2]
# reportid = IsreportIDvalid(data)
# uidate = data['rows'][0][5]
if (data['rows'][0][0] == queryname):
    checkEqualAssert(data['rows'][0][0],queryname,"Today","","Netflow Query name")
    checkEqualAssert(data['rows'][0][3],date,"Today","","Time of the Netflow Query")
else:
    forensicsScreenHandle = getHandle(setup,"forensics_Screen")
    forensicsScreenInstance.switcher.switchTo(0,forensicsScreenHandle,'createdialog','switcher')
    forensicsScreenHandle = getHandle(setup,"forensics_Screen")
    data = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"netflowtable")
    checkEqualAssert(data['rows'][0][0],queryname,"Today","","Netflow Query name")
    checkEqualAssert(data['rows'][0][2],date,"Today","","Time of the Netflow Query")








# Closing the Testcase
setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
