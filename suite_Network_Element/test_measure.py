import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Components.SwitcherComponentClass import *
# Getting Setup Details and Launching the application

setup = SetUp()
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
print quicklinks
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
print measureIteration
measures = setup.cM.getNodeElements("measures","measure").keys()
print measures



# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

#set timerange and measure
# setTimeRange(setup,"TODAY")
# setMeasure(setup,"Flows_uplink_percentage_average","site_Screen")
# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

test_case1="Default selection of site screen"
# Get the default selection
# defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
# checkEqualAssert(str(1),str(defSelection['selIndex']),"Today","Flows",test_case1)

# Set the bar Table view to the 2 index
a = screenInstance.btv.setSelection(2,siteScreenHandle)
# defSelection = screenInstance.btv.getSelection(siteScreenHandle)
# data=screenInstance.btv.getData(siteScreenHandle)
status=drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)
print status
test_case2 ="Drill TO Network Element Screen"
checkEqualAssert("True",str(status),"Today","Flows",test_case2)

neScreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

#Check single and multiple selection on pielegend
# Selection_list=[[1]]
#for i in Selection_list:
#    neScreenInstance.pielegend.setSelection(setup.dH,i,neScreenHandle)
#    neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
#    test_case5="Check Selection of pieLegend in NE screen"
#    piedata = neScreenInstance.pielegend.getData(neScreenHandle)
#    piedata['tooltipdata'] = neScreenInstance.pie.getToolTipInfo(setup.d, setup.dH, neScreenHandle)
    #checkEqualAssert(str(i),str(deflegendSel['selIndices']),set_time,set_measure,test_case5)


while t < timeIteration:
    i=0
    # setTimeRange(setup,quicklinks[t])
    screenInstance.quiklinkTimeRange.setSelection(quicklinks[t], neScreenHandle)

    # while loop is to iterate over all the measure
    while i < measureIteration:
        print measures[i]
        neScreenHandle1 = getHandle(setup, Constants.NETWORKELEMENTS)
        status=screenInstance.measure.doSelection(neScreenHandle1, measures[i])
        checkEqualAssert("True", str(status), quicklinks[t], measures[i], "Measure selection")
        # setMeasure(setup,measures[i],"ne_Screen")
        neScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)
        #print neScreenHandle
        # neScreenInstance.pielegend.setSelection(setup.dH, [3], neScreenHandle)

        piedata = neScreenInstance.pielegend.getData(neScreenHandle)
        piedata['tooltipdata'] = neScreenInstance.pie.getToolTipInfo(setup.d, setup.dH, neScreenHandle)
        print piedata
        checkEqualAssert(piedata['legendText'], piedata['tooltipdata'], quicklinks[t], measures[i],"Pie Tooltip Validations at NFScreen for " + measures[i])

        i+=1
    t+=1

setup.d.close()