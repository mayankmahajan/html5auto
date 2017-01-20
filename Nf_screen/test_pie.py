import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.NETWORKFUNCTIONS)

# Get the Instance of the nf screen
nfScreenInstance = NFPageClass(setup.d)

# Get the handles of the nf screenx
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)

# GetSelection
defaultSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
print defaultSelection
# Log Result
#to check def selection of pielegend that should  be null
checkEqualAssert([],defaultSelection['selIndices'],"","","Null Default Selection at NFScreen for pielegend")

#def selection of pie
#defpieSel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
#checkEqualAssert([0],defpieSel['selIndices'],"","","Null")


#single selection on pielegend

nfScreenInstance.pielegend.setSelection(setup.dH, [2], nfScreenHandle)

#get the selection on pie
pieSelections = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
#print pieSelections

#get selection on legend
updatedSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
#print  updatedSelection

#match if it is 2nd one
checkEqualAssert([2],updatedSelection['selIndices'],"","","Match Selection  b/w pie and legend is 2")



#Multiple selection at pie legend and validation
nfScreenInstance.pielegend.setSelection(setup.dH, [1,2,3], nfScreenHandle)

#get pielegend multiple selection in a var
mulpielegsel =nfScreenInstance.pielegend.getSelection(nfScreenHandle)
#print mulpielegsel
#get selections at pie due to set selection at legend
mulpiesel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
#print mulpiesel

#match
checkEqualAssert([1,2,3],mulpielegsel['selIndices'],"","","Match Selection b/w pie and legend is 1,2,3")


# GetChartData
piedata = nfScreenInstance.pielegend.getData(nfScreenHandle)
print piedata
# GetTooltipData
piedata['tooltipdata'] = nfScreenInstance.pie.getToolTipInfo(setup.d,setup.dH,nfScreenHandle)
print piedata

# Log Result
checkEqualAssert(piedata['legendText'],piedata['tooltipdata'],"","","Pie Tooltip Validations at NFScreen")

# Closing the Testcase
setup.d.close()

