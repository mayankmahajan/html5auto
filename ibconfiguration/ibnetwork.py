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
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","nf_Screen")

exploreScreenInstance.exploreList.switchApp(exploreHandle,1)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])
confScreenInstance = ConfigurationPageClass(setup.d)
confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.leftColumn.select(1,confScreenHandle)
confScreenHandle = getHandle(setup,"configuration_Screen")

confScreenInstance.dummyelement.doSelection(confScreenHandle,"Name",'searchSelector','select')
confScreenInstance.dummyelement.doSelection(confScreenHandle,"NetworkElement1",'searchSelector','select')
confScreenInstance.dummyelement.doSelection(confScreenHandle,"NetworkElement2",'searchSelector','select')
confScreenInstance.dummyelement.doSelection(confScreenHandle,"Port",'searchSelector','select')
confScreenInstance.dummyelement.doSelection(confScreenHandle,"Protocol",'searchSelector','select')


confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])

createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")

# Bulk Upload ##
createPopInstance.switcher.switchTo(1,createPopHandle,'createdialog','switcher')
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['choosefile'],"/Users/deepanshu.ahuja/Documents/nfib.csv")
createPopInstance.dropdown.customClick(createPopHandle['createdialog']['upload'])




confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['nfName'],"nfautomation")
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','networkElement1')
createPopInstance.dropdown.doSelection(createPopHandle,"HA",'createdialog','networkElement2')
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['port'],"12")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['protocol'],"23")
createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])


confScreenHandle = getHandle(setup,"configuration_Screen")


confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][3])
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][4])
confScreenHandle = getHandle(setup,"configuration_Screen")
# Delete is not working now
confScreenInstance.table.setSelection1(3,confScreenHandle,"table")
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][1])


confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.table.setSelection1(1,confScreenHandle,"table")
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][2])
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['nfName'],"nfautomationHost1")
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','networkElement1')
createPopInstance.dropdown.doSelection(createPopHandle,"HA",'createdialog','networkElement2')
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['port'],"12")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['protocol'],"23")
createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])

# confScreenHandle = getHandle(setup,"configuration_Screen")




setup.d.close()