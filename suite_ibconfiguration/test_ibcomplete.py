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

exploreScreenInstance.exploreList.switchApp(exploreHandle)
result =exploreScreenInstance.exploreList.launchapp(getHandle(setup,"explore_Screen"),1)
time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])
checkEqualAssert(result,True,"","","Launch IB Configuration Validation")
confScreenInstance = ConfigurationPageClass(setup.d)
confScreenHandle = getHandle(setup,"configuration_Screen")


createopen = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
checkEqualAssert(createopen,True,"","","Create Dialog Box Validation")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")

# Bulk Upload ##
createPopInstance.switcher.switchTo(1,createPopHandle,'createdialog','switcher')
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['choosefile'],"/Users/deepanshu.ahuja/Documents/siteib.csv")
upload = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['upload'])
checkEqualAssert(upload,True,"","","OK Dialog box Validation")
createPopHandle = getHandle(setup, "config_popup","successdialog")
Upload = createPopInstance.reportspopup.clickButton("Ok",createPopHandle)
checkEqualAssert(Upload,True,"","","Bulk uploaded Validation")



confScreenHandle = getHandle(setup,"configuration_Screen")
create = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
checkEqualAssert(create,True,"","","Create Dialog box Validation")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['hostName'],"automationHost1")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['ipAddress'],"192.168.115.113")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['newSiteName'],"automationSite1")
createPopInstance.dropdown.doSelection(createPopHandle,"Cell Site",'createdialog','siteType')
createPopInstance.dropdown.doSelection(createPopHandle,"eNB",'createdialog','elementType')
createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])


confScreenHandle = getHandle(setup,"configuration_Screen")


confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][3])
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][4])
confScreenHandle = getHandle(setup,"configuration_Screen")
# Delete is not working now
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
##############################Delete Completion ####################################

confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.table.setSelection1(3,confScreenHandle,"table")
edit = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][2])
checkEqualAssert(edit,True,"","","Edit Dialog box Opens")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['hostName'],"automationHost1")
createPopInstance.dropdown.doSelection(createPopHandle,"WDC",'createdialog','siteType')
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','elementType')
editbutton = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])
checkEqualAssert(editbutton,True,"","","Edit button functionality Validation")
confScreenHandle = getHandle(setup,"configuration_Screen")

nfconfiguration = confScreenInstance.leftColumn.select(1,confScreenHandle)
checkEqualAssert(nfconfiguration,True,"","","Network Function IB configuration Validation")
########################### NETWORK FUNCTION IB CONFIGURATION ###############################################

time.sleep(10)
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
setup.d.switch_to_alert().accept()


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
######################## NETWORK FUNCTION IB CONFIGURATION END ########################################

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
