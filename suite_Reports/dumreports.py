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
setup.d.switch_to.window(setup.d.window_handles[1])
popupInstance = GenerateReportsPopClass(setup.d)
popupHandler = getHandle(setup,"routers_popup","queryrouters")

popupHandler['queryrouters']['starttime'][0].click()
setCalendar("2016","March","24","02","10",popupInstance,setup)
popupHandler = getHandle(setup,"routers_popup","allbuttons")
popupInstance.reportspopup.clickButton("Apply",popupHandler)
popupHandler = getHandle(setup,"routers_popup","queryrouters")
popupHandler['queryrouters']['endtime'][0].click()
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
setup.d.close()