import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Components.SwitcherComponentClass import *


#######################################################################
# Getting Setup Details
setup = SetUp()
#######################################################################


#######################################################################
#get time range and measures from config file
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0

measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()
#######################################################################

#######################################################################
# Logging into the appliction and launch site screen
login(setup, "admin", "Admin@123")
launchPage(setup,"site_Screen")
sleep(5)
#######################################################################


#######################################################################
# get screen instance and set timerange and measure and Get the handles of the screen
set_measure=measures[0]
set_time=quicklinks[0]
screenInstance = SitePageClass(setup.d)
setTimeRange(setup,set_time)
setMeasure(setup,set_measure,"site_Screen")
siteScreenHandle = getHandle(setup,"site_Screen")
#######################################################################

#######################################################################
# Get the default selection and Validate the result
test_case1="Default selection of site screen"
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
checkEqualAssert(str(1),str(defSelection['selIndex']),set_time,set_measure,test_case1)
#######################################################################


#######################################################################
# Set the bar Table view to the 2 index and validate the result
a = screenInstance.btv.setSelection(2,siteScreenHandle)
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
data=screenInstance.btv.getData(siteScreenHandle)
status=drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)
test_case2 ="Drill TO Network Element Screen"
checkEqualAssert("True",str(status),set_time,set_measure,test_case2)
#######################################################################

#######################################################################
#Create screen instance and get handle of screen
neScreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
#######################################################################


#######################################################################
#VAR=neScreenInstance.switcher.getSelection(neScreenHandle)
#test_case2="Default Selection in chart"
#checkEqualAssert("Chart",str(status),set_time,set_measure,test_case3)
#######################################################################


#######################################################################
# Get the default selection of ne screen
deflegendSel = neScreenInstance.pielegend.getSelection(neScreenHandle)
defpieSel = neScreenInstance.pie.getPieSelections(neScreenHandle)
test_case4="Default Selection of pieLegend in NE screen"
checkEqualAssert(str("[]"),str(deflegendSel['selIndices']),set_time,set_measure,test_case4)
#######################################################################

#######################################################################
#Check single and multiple selection on pielegend
Selection_list=[[1],[1,2,3]]
for i in Selection_list:
    neScreenInstance.pielegend.setSelection(setup.dH,i,neScreenHandle)
    neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
    deflegendSel = neScreenInstance.pielegend.getSelection(neScreenHandle)
    defpieSel = neScreenInstance.pie.getPieSelections(neScreenHandle)
    test_case5="Check Selection of pieLegend in NE screen"
    checkEqualAssert(str(i),str(deflegendSel['selIndices']),set_time,set_measure,test_case5)
#######################################################################

#######################################################################
#Get chart data and tooltip data
test_case6="Pie Tooltip Validations at NFScreen"
piedata = neScreenInstance.pielegend.getData(neScreenHandle)
piedata['tooltipdata'] = neScreenInstance.pie.getToolTipInfo(setup.d,setup.dH,neScreenHandle)
checkEqualAssert(piedata['legendText'],piedata['tooltipdata'],set_time,set_measure,test_case6)
#######################################################################


#######################################################################
#measuse and time range selection and data validation
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        print measures[i]
        setMeasure(setup,measures[i],"ne_Screen")
        neScreenHandle={}
        neScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)
        pidata1={}
        piedata1 = neScreenInstance.pielegend.getData(neScreenHandle)
        piedata1['tooltipdata'] = neScreenInstance.pie.getToolTipInfo(setup.d, setup.dH, neScreenHandle)
        print piedata
        checkEqualAssert(piedata1['legendText'], piedata1['tooltipdata'], quicklinks[t], measures[i],"Pie Tooltip Validations at NFScreen for " + measures[i])

        i+=1
    t+=1

#######################################################################


#######################################################################
#search box testing on ne screen
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
piedata=neScreenInstance.pielegend.getData(neScreenHandle)
text=["p","","mm","","G","hfgjghkkkhjk"]
click=["one","two"]

for word in text:
    expected_search_result=[piedata["legendText"][i] for i in range(0,len(piedata["legendText"])) if piedata["legendText"][i].lower().find(word.lower()) >= 0 and piedata["legendText"][i].lower().find(word.lower()) < piedata["legendText"][i].lower().find("\n")]
    setSearch = neScreenInstance.searchComp.setSearchText(neScreenHandle,word)
    time.sleep(5)
    if(setSearch==True):
     for click_times in click:
        if click_times == "one":
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
        elif click_times == "two":
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
            expected_search_result = piedata["legendText"]

        neScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)
        search_pie_result=neScreenInstance.pielegend.getData(neScreenHandle)
        print search_pie_result
        checkEqualAssert(expected_search_result, search_pie_result["legendText"], "", "", "Search_passed_for_"+str(word)+str(click))
    else:
     checkEqualAssert(False, setSearch, set_time,set_measure, "Search_passed_for_word_"+str(word))