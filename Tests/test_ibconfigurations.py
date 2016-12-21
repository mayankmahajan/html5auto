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


confScreenInstance.dummyelement.click(confScreenHandle['buttons']['crudbuttons'][0])


createPopInstance = GenerateReportsPopClass(setup.d)
createPopHandle = getHandle(setup, "config_popup")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['hostName'],"automationHost1")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['ipAddress'],"192.168.115.113")
createPopInstance.dropdown.customSendkeys(createPopHandle['createdialog']['newSiteName'],"automationSite1")
createPopInstance.dropdown.doSelection(createPopHandle,"Cell Site",'createdialog','siteType')
createPopInstance.dropdown.doSelection(createPopHandle,"eNB",'createdialog','elementType')
createPopInstance.dropdown.customClick(createPopHandle['createdialog']['submit'])

confScreenHandle = getHandle(setup,"configuration_Screen")

confScreenInstance.dummyelement.doSelection(confScreenHandle,"IP",'searchSelector','select')
confScreenInstance.searchComp.setSearchText(confScreenHandle,"192.168.115.113")
confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)


confScreenInstance.leftColumn.select(1,confScreenHandle)


# getdata from table and check whether it is created or not





# createPopInstance.dropdown.doSelection(createPopHandle, "Average", "generateReportDialog", "measureType")




# grPopHandle = getHandle(setup,"report_popup")
#
#
# filters = grPopInstance.dropdown.customText(grPopHandle['generateReportDialog']["filters"])
# grPopInstance.dropdown.doSelection(grPopHandle,"Average","generateReportDialog","measureType")
# grPopInstance.dropdown.doSelection(grPopHandle,"Yesterday","generateReportDialog","quicklink")
# grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],"report1")
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
# grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],"mayank.mahajan@guavus.com")
# grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["generate"])
# grPopHandle = getHandle(setup,"report_popup")
# grPopInstance.dropdown.customClick(grPopHandle['successdialog']["ok"])


# Closing the Testcase
setup.d.close()