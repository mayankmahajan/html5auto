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

exploreScreenInstance.exploreList.switchApp(exploreHandle)
result = exploreScreenInstance.exploreList.launchapp(getHandle(setup,"explore_Screen"),2)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])




forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen","commoncomponents")

forensicsScreenInstance.dummyelement.customClick(forensicsScreenHandle['commoncomponents']['newquery'])

popupInstance = GenerateReportsPopClass(setup.d)
####### Get the Handles of the routers Popup#################
popupHandler = getHandle(setup,"routers_popup","queryrouters")

############# Get the calendar Dialog box open ##################
popupHandler['queryrouters']['starttime'][0].click()
############# Set the Start time ##################
setCalendar("2016","March","24","02","10",popupInstance,setup)
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Apply",popupHandler)
popupHandler = getHandle(setup,"routers_popup","queryrouters")



popupHandler['queryrouters']['endtime'][0].click()
############## Get the endtime Dialog Box open####################
setCalendar("2016","March","24","02","10",popupInstance,setup)
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Apply",popupHandler)



popupHandler = getHandle(setup,"routers_popup","queryrouters")
queryName = popupInstance.routerpopup.setQueryName(queryname,popupHandler,'queryrouters','wizard1')
sortBy = popupInstance.routerpopup.setSortBy("PROTOCOL",popupHandler,'queryrouters','wizard1')
sortOrder = popupInstance.routerpopup.setSortOrder("ASC",popupHandler,'queryrouters','wizard1')
pageSize = popupInstance.routerpopup.setPageSize("500",popupHandler,'queryrouters','wizard1')



popupHandler = getHandle(setup,"routers_popup","routertable")
popupInstance.routertable.setSelection1(2,popupHandler,'routertable')



popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Next Step",popupHandler)



popupHandler = getHandle(setup,"routers_popup","wizards")
addrule =popupInstance.routerpopup.add("addrule",popupHandler)
popupInstance.routerpopup.add("addrule",popupHandler,0)
popupInstance.routerpopup.add("addrule",popupHandler,0)
addgroup =popupInstance.routerpopup.add("addgroup",popupHandler,0)
popupInstance.routerpopup.add("addrule",popupHandler,1)
popupInstance.routerpopup.add("addgroup",popupHandler,1)
popupInstance.routerpopup.add("addrule",popupHandler,2)
deletegroup =popupInstance.routerpopup.add("deletegroup",popupHandler,1)
deleterule = popupInstance.routerpopup.add("deleterule",popupHandler,1)
popupInstance.routerpopup.updateGroup("rule",["DST PORT","in",2],popupHandler)
popupInstance.routerpopup.updateGroup("rule",["DST PORT","in",2],popupHandler,2)



checkEqualAssert(addrule,True,"","","Add Rule Validation")
checkEqualAssert(addgroup,True,"","","Add Group Validation")
checkEqualAssert(deleterule,True,"","","Delete Rule Validation")
checkEqualAssert(deletegroup,True,"","","Delete Group Validation")
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Submit Query",popupHandler)
date = currentdate()
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Ok",popupHandler)
forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")
forensicsScreenInstance.switcher.switchTo(1,forensicsScreenHandle,'createdialog','switcher')
forensicsScreenHandle = getHandle(setup,"forensics_Screen","netflowtable")

data = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"netflowtable")
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
