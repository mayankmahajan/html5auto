import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.QuickTrendsPageClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

screen_name='site_Screen'
# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,screen_name)

VAR=screenInstance.switcher.getSelection(siteScreenHandle)
# test_case2="Default Selection in chart"
# checkEqualAssert("Chart",str(status),set_time,set_measure,test_case3)


# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)

# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"","","Checking the Default selection of the bar tabler view")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
drillnf = drilltoScreen(setup.d,setup.dH,Constants.NETWORKFUNCTIONS)
checkEqualAssert(drillnf,True,"","","Checking the drill to functionality to the Network Function")

nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle =getHandle(setup,Constants.NETWORKFUNCTIONS)

#nfScreenInstance.pielegend.setSelection(setup.dH, [2], nfScreenHandle)

nfScreenInstance.cm.activateContextMenuOptions1(nfScreenHandle)

nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS,"cm")
launchtrends = nfScreenInstance.cm.launchTrends(nfScreenHandle)
checkEqualAssert(launchtrends,True,"","","Checking the launch page of quick Trends")
qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")
list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
print list
xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)



t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle,setup)
######## Toolip validation in quicktrends is still not implementing ####################
# Closing the Testcase
setup.d.close()