from MuralUtils import AlertsHelper
from MuralUtils.MuralConstants import *
from Utils.SetUp import *
from Utils.utility import *

setup = SetUp()

login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

print isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")


popInstance = GenerateReportsPopClass(setup.d)
# Launching Settings Page
popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
popInstance.switcher.switchTo(0,getHandle(setup,MuralConstants.ALERTSCREEN,"settings"),"settings")

print isError(setup)
# columns = ["DPI Alert Rule Name","Frequency","Measure","Range","Status"]
columnName = "DPI Alert Rule Name"

print AlertsHelper.deleteTableEntry(setup,MuralConstants.ALERTSCREEN,1,columnName)
# print AlertsHelper.deleteTableEntry(setup,MuralConstants.ALERTSCREEN,0,columnName,False)
# print AlertsHelper.editAlert(setup, 0,columnName)





# Closing the browser
setup.d.close()