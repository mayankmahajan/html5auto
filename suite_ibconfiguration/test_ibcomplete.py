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
checkEqualAssert(result,True,"","","Checking the IB Configuration launch button")
confScreenInstance = ConfigurationPageClass(setup.d)
confScreenHandle = getHandle(setup,"configuration_Screen")


createopen = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
checkEqualAssert(createopen,True,"","","Checking the functionality of Create Button at the IB configuration Screen")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")

# Bulk Upload ##
switcher = createPopInstance.switcher.switchTo(1,createPopHandle,'createdialog','switcher')
checkEqualAssert(switcher,True,"","","Checking the functionality of the switcher in the Create Dialog Box at the IB configuration Screen")
createPopHandle = getHandle(setup, "config_popup")
# import os
# currentPath = os.system("echo $(pwd)")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['choosefile'],"/Users/deepanshu.ahuja/html5automation/suite_ibconfiguration/siteib.csv")
upload = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['upload'])
checkEqualAssert(upload,True,"","","Checking the Upload button Functionality at the IB configuration Screen")
# createPopHandle = getHandle(setup, "config_popup","successdialog")
# Upload = createPopInstance.reportspopup.clickButton("Ok",createPopHandle)
# checkEqualAssert(Upload,True,"","","Checking the Bulk upload file at the IB configuraton Screen")



confScreenHandle = getHandle(setup,"configuration_Screen")
create = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
checkEqualAssert(create,True,"","","Checking Create Button at the IB configuration Screen")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['hostName'],"automationHost5")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['ipAddress'],"192.168.115.113")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['newSiteName'],"automationSite1")
createPopInstance.dropdown.doSelection(createPopHandle,"Cell Site",'createdialog','siteType')
createPopInstance.dropdown.doSelection(createPopHandle,"eNB",'createdialog','elementType')
submit = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])
checkEqualAssert(submit,True,"","","Checking the functionality of the submit button of the file uploaded at the IB configuration Screen ")

confScreenHandle = getHandle(setup,"configuration_Screen")


refresh = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][3])
checkEqualAssert(refresh,True,"","","Checking the functionality of the Refresh button at the IB configuration Screen")
export =confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][4])
checkEqualAssert(export,True,"","","Checking the functionality of the Export button at the IB Configuration Screen")
confScreenHandle = getHandle(setup,"configuration_Screen")
# Delete is not working now
dropdown =confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
checkEqualAssert(dropdown,True,"","","Checking the Dropdown menu at the IB configuraion Screen")
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
checkEqualAssert(search,False,"","","Checking the Delete Functionality at the IB Configuration Screen")
##############################Delete Completion ####################################

confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.table.setSelection1(3,confScreenHandle,"table")
edit = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][2])
checkEqualAssert(edit,True,"","","Checking the edit button functionality at the IB configuration Screen")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
############### Has to update the edit validation in the script ##################
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['hostName'],"automationHost1")
createPopInstance.dropdown.doSelection(createPopHandle,"WDC",'createdialog','siteType')
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','elementType')
editbutton = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])
checkEqualAssert(editbutton,True,"","","Checking the edit fields at the IB configuration")
confScreenHandle = getHandle(setup,"configuration_Screen")

nfconfiguration = confScreenInstance.leftColumn.select(1,confScreenHandle)
checkEqualAssert(nfconfiguration,True,"","","Checking the functionality of Network Function IB configuration Tab at IB configuration Screen")




########################### NETWORK FUNCTION IB CONFIGURATION ###############################################

time.sleep(10)
confScreenHandle = getHandle(setup,"configuration_Screen")

# confScreenInstance.dummyelement.doSelection(confScreenHandle,"Name",'searchSelector','select')
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"NetworkElement1",'searchSelector','select')
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"NetworkElement2",'searchSelector','select')
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"Port",'searchSelector','select')
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"Protocol",'searchSelector','select')


createopen = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
checkEqualAssert(createopen,True,"","","Checking the create Button at the Network Function IB configuration Screen")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")

# Bulk Upload ##
switcher = createPopInstance.switcher.switchTo(1,createPopHandle,'createdialog','switcher')
checkEqualAssert(switcher,True,"","","Checking the switcher in the Create Dialog Box at the Network IB configuration Screen")


createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['choosefile'],"/Users/deepanshu.ahuja/html5automation/suite_ibconfiguration/nfib.csv")
upload = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['upload'])
checkEqualAssert(upload,True,"","","Checking the Upload button Functionality at the Network IB configuration Screen")
# createPopHandle = getHandle(setup, "config_popup","successdialog")
# Upload = createPopInstance.reportspopup.clickButton("Ok",createPopHandle)
# checkEqualAssert(Upload,True,"","","Checking the Bulk upload file at the Network IB configuraton Screen")




confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['nfName'],"nfautomation")
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','networkElement1')
createPopInstance.dropdown.doSelection(createPopHandle,"HA",'createdialog','networkElement2')
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['port'],"12")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['protocol'],"23")
submit = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])
checkEqualAssert(submit,True,"","","Checking the functionality of the submit button of the file uploaded at the Network IB configuration Screen ")

confScreenHandle = getHandle(setup,"configuration_Screen")



refresh = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][3])
checkEqualAssert(refresh,True,"","","Checking the functionality of the Refresh button at the Network IB configuration Screen")
export =confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][4])
checkEqualAssert(export,True,"","","Checking the functionality of the Export button at the Network IB Configuration Screen")
confScreenHandle = getHandle(setup,"configuration_Screen")

# # Delete is not working now
# dropdown = confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
# checkEqualAssert(dropdown,True,"","","Checking the Dropdown menu at the IB configuraion Screen")
# confScreenInstance.searchComp.setSearchText(confScreenHandle,"3.3.3.3")
# confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
# confScreenHandle = getHandle(setup,"configuration_Screen")
#
# confScreenInstance.table.setSelection1(1,confScreenHandle,"table")
# confScreenHandle = getHandle(setup,"configuration_Screen","buttons")
# confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][1])
# setup.d.switch_to_alert().accept()
# confScreenHandle = getHandle(setup,"configuration_Screen")
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"Site",'searchSelector','select')
# confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
# confScreenInstance.searchComp.setSearchText(confScreenHandle,"3.3.3.3")
# confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
# confScreenHandle = getHandle(setup,"configuration_Screen","table")
# data = confScreenInstance.table.getTableData1(confScreenHandle,"table")
#
# search = validatesearchtable(data,"IP","3.3.3.3")
# checkEqualAssert(search,False,"","","Checking the Delete Functionality at the IB Configuration Screen")
# ##############################Delete Completion ####################################


confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.table.setSelection1(1,confScreenHandle,"table")
edit = confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][2])
checkEqualAssert(edit,True,"","","Checking the edit button functionality at the Network IB configuration Screen")
createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['nfName'],"nfautomationHost1")
createPopInstance.dropdown.doSelection(createPopHandle,"FA",'createdialog','networkElement1')
createPopInstance.dropdown.doSelection(createPopHandle,"HA",'createdialog','networkElement2')
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['port'],"12")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['protocol'],"23")
edit = createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])
checkEqualAssert(editbutton,True,"","","Checking the edit fields at the Network IB configuration")

######################## NETWORK FUNCTION IB CONFIGURATION END ########################################

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
