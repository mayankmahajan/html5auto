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
# columnname = ["Site","IP","Host Name","Site Type","Element Type"]
# # columnname = ["Element Type"]
# searchtext = ["Akron","1.1","enB","WDC","IPA" ]
# # searchtext = ["IPA" ]
# for i in range(len(columnname)):
#
#     confScreenInstance.dummyelement.doSelection(confScreenHandle,columnname[i],'searchSelector','select')
#     confScreenInstance.searchComp.setSearchText(confScreenHandle,searchtext[i])
#     confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
#     confScreenHandle = getHandle(setup,"configuration_Screen")
#
#     data = confScreenInstance.table.getTableData1(confScreenHandle,"table")
#
#     search = validatesearchtable(data,columnname[i],searchtext[i])
#     message = columnname[i] + "" + "search is verified"
#     checkEqualAssert(search,True,"","",message)
#
confScreenHandle = getHandle(setup,"configuration_Screen")
confScreenInstance.leftColumn.select(1,confScreenHandle)
confScreenHandle = getHandle(setup,"configuration_Screen")

networkcolumnname = ["Name","NetworkElement1","NetworkElement2","Port","Protocol"]
networksearchtext = ["s","s","p","a","b"]
for i in range(len(networkcolumnname)):

    confScreenInstance.dummyelement.doSelection(confScreenHandle,networkcolumnname[i],'searchSelector','select')
    confScreenInstance.searchComp.setSearchText(confScreenHandle,networksearchtext[i])
    confScreenInstance.searchComp.hitSearchIcon(confScreenHandle)
    confScreenHandle = getHandle(setup,"configuration_Screen")

    data = confScreenInstance.table.getTableData1(confScreenHandle,"table")

    search = validatesearchtable(data,networkcolumnname[i],networksearchtext[i])
    message = networkcolumnname[i] + "" + "search is verified"
    checkEqualAssert(search,True,"","",message)



setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()