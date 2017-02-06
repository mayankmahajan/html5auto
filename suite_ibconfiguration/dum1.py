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
confScreenHandle = getHandle(setup,"configuration_Screen","buttons")
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

setup.d.close()