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
checkEqualAssert(result,True,"","","Checking the launching of Netflow Forensics UI")

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])




forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen","commoncomponents")

newquery =forensicsScreenInstance.dummyelement.customClick(forensicsScreenHandle['commoncomponents']['newquery'])
checkEqualAssert(newquery,True,"","","Checking the functionality of the new query button at Netflow Forensics Screen")

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



checkEqualAssert(addrule,True,"","","Checking the functionality of the Add Rule button at the Netflow Forensic Screen")
checkEqualAssert(addgroup,True,"","","Checking the functionality of the Add Group button at the Netflow Forensic Screen")
checkEqualAssert(deleterule,True,"","","Checking the functionality of the Delete Rule button at the Netflow Forensic Screen")
checkEqualAssert(deletegroup,True,"","","Checking the functionality of the Delete Group button at the Netflow Forensic Screen")
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Submit Query",popupHandler)
date = currentdate()
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Ok",popupHandler)
forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen","createdialog")
forensicsScreenInstance.switcher.switchTo(1,forensicsScreenHandle,'createdialog','switcher')
forensicsScreenHandle = getHandle(setup,"forensics_Screen","netflowtable")

data = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"netflowtable")
# result = data['rows'][0][1]
# type = data['rows'][0][2]
# reportid = IsreportIDvalid(data)
# uidate = data['rows'][0][5]
if (data['rows'][0][0] == queryname):
    checkEqualAssert(data['rows'][0][0],queryname,"Today","","Checking the name of the Netflow Query at the Pending Tab")
    checkEqualAssert(data['rows'][0][3],date,"Today","","Checking the Requested Time of the Netflow Query at the Pending Tab")
else:
    forensicsScreenHandle = getHandle(setup,"forensics_Screen")
    forensicsScreenInstance.switcher.switchTo(0,forensicsScreenHandle,'createdialog','switcher')
    forensicsScreenHandle = getHandle(setup,"forensics_Screen")
    data = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"netflowtable")
    checkEqualAssert(data['rows'][0][0],queryname,"Today","","Checking the name of the Netflow Query at the Completed Tab")
    checkEqualAssert(data['rows'][0][2],date,"Today","","Checking the time of the Netflow Query at the Completed Tab")








# Closing the Testcase
setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
