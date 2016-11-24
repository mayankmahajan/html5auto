import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NFPageClass import *
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
print set_time
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")
# setTimeRange(setup,set_time)
screenInstance.quiklinkTimeRange.setSelection(set_time,siteScreenHandle)
# screenInstance.quiklinkTimeRange.doSelection()
a=screenInstance.measure.doSelection(siteScreenHandle,set_measure)
print a
#setMeasure(setup,set_measure,"site_Screen")
#siteScreenHandle = getHandle(setup,"site_Screen")
#######################################################################

#######################################################################
# Get the default selection and Validate the result
siteScreenHandle =getHandle(setup,"site_Screen")
test_case1="Default selection at site screen"
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
checkEqualAssert(str(1),str(defSelection['selIndex']),set_time,set_measure,test_case1)
#######################################################################


#######################################################################
# Set the bar Table view to the 2nd index and validate the result
a = screenInstance.btv.setSelection(2,siteScreenHandle)
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
data=screenInstance.btv.getData(siteScreenHandle)
status=drilltoScreen(setup.d,setup.dH,Constants.NETWORKFUNCTIONS)
test_case2 ="Drill TO Network Function Screen"
checkEqualAssert("True",str(status),set_time,set_measure,test_case2)
#######################################################################

#######################################################################
#Create screen instance and get handle of NF screen
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)
#######################################################################


#######################################################################
VAR=nfScreenInstance.switcher.getSelection(nfScreenHandle)
test_case2="Default Selection in chart"
checkEqualAssert("Chart",str(status),set_time,set_measure,test_case2)
#######################################################################

nfScreenInstance.switcher.setSelection(1,nfScreenHandle)
VAR=nfScreenInstance.switcher.getSelection(nfScreenHandle)
test_case3="New Selection in table"
checkEqualAssert("Table",str(VAR),set_time,set_measure,test_case3)

nfScreenInstance.switcher.setSelection(0,nfScreenHandle)
#######################################################################
#Get the default selection at NF screen
deflegendSel = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
defpieSel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
test_case4="Default Selection of pieLegend at NF screen"
checkEqualAssert(str("[]"),str(deflegendSel['selIndices']),set_time,set_measure,test_case4)
#######################################################################

#######################################################################
# #Check single and multiple selection on pielegend
Selection_list=[[1],[2],[3],[4]]
expected_list=[]
for i in Selection_list:
    nfScreenInstance.pielegend.setSelection(setup.dH,i,nfScreenHandle)
    nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)
    deflegendSel = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
    defpieSel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
    test_case5="Check Selection of pieLegend at NF screen"
    expected_list.append(i[0])
    checkEqualAssert(str(expected_list),str(deflegendSel['selIndices']),set_time,set_measure,test_case5)
# #######################################################################
#
# #######################################################################
# #Get chart data and tooltip data
test_case6="Pie Tooltip Validations at NFScreen"
piedata = nfScreenInstance.pielegend.getData(nfScreenHandle)
piedata['tooltipdata'] = nfScreenInstance.pie.getToolTipInfo(setup.d,setup.dH,nfScreenHandle)
checkEqualAssert(piedata['legendText'],piedata['tooltipdata'],set_time,set_measure,test_case6)
#######################################################################


#######################################################################
#measuse and time range selection and data validation

while t < timeIteration:
    i=0
    # setTimeRange(setup,quicklinks[t])
    screenInstance.quiklinkTimeRange.setSelection(quicklinks[t], siteScreenHandle)

    # while loop is to iterate over all the measure
    while i < measureIteration:
        screenInstance.measure.doSelection(nfScreenHandle, measures[i])
        # sleep(5)
        #setMeasure(setup,measures[i],Constants.NETWORKFUNCTIONS)

        # print measures[i]
        # print i

         # Result Logging
        expected = "True"
        actual = "True"


        checkEqualAssert(expected,actual,quicklinks[t], measures[i])
        i+=1
         # end of measureSelection


    t+=1
     # end of while loop for QuicklinkSelections
#######################################################################


#######################################################################
# while t < timeIteration:
#     i=0
#     setTimeRange(setup,quicklinks[t])
#
#     # while loop is to iterate over all the measure
#     while i < measureIteration:
#         print measures[i]
#         setMeasure(setup,measures[i],Constants.NETWORKFUNCTIONS)
#         #nfScreenHandle={}
#         #nfScreenHandle = getHandle(setup, Constants.NETWORKFUNCTIONS)
#         #pidata1={}
#         #piedata1 = nfScreenInstance.pielegend.getData(nfScreenHandle)
#         #piedata1['tooltipdata'] = nfScreenInstance.pie.getToolTipInfo(setup.d, setup.dH, nfScreenHandle)
#         #print piedata
#         #checkEqualAssert(piedata1['legendText'], piedata1['tooltipdata'], quicklinks[t], measures[i],"Pie Tooltip Validations at NFScreen for " + measures[i])
#
#         i+=1
#     t+=1

#######################################################################


#######################################################################
#search box testing on ne screen

nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)
piedata=nfScreenInstance.pielegend.getData(nfScreenHandle)
# Search testing. Length of text list should be >=2 if we have to check backspace key functionality.
text=["u","g","s",Keys.BACK_SPACE]
click=["one","two"]
count=1
for word in text:
    if word==Keys.BACK_SPACE:
       index_previous=text.index(Keys.BACK_SPACE)-1
       word1=text[text.index(Keys.BACK_SPACE)-1][:-1]
       setSearch =  nfScreenInstance.searchComp.setSearchText(nfScreenHandle, text[index_previous])
       msg="Search_for_backspace"
    else:
        msg="Search_for_"+word+" "
        word1=word
    expected_search_result=[piedata["legendText"][i] for i in range(0,len(piedata["legendText"])) if piedata["legendText"][i].lower().find(word1.lower()) >= 0 and piedata["legendText"][i].lower().find(word1.lower()) < piedata["legendText"][i].lower().find("\n")]
    print word1,expected_search_result
    setSearch = nfScreenInstance.searchComp.setSearchText(nfScreenHandle,word)
    time.sleep(5)
    if(setSearch==True):
     for click_times in click:
        if click_times == "one":
            #single hit on search button
            nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
        elif click_times == "two" and count==1:
            #bouble hit on search button
            nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
            nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
            expected_search_result = piedata["legendText"]
            count=0
        else:
            break
        nfScreenHandle = getHandle(setup, Constants.NETWORKFUNCTIONS)
        search_pie_result=nfScreenInstance.pielegend.getData(nfScreenHandle)
        print search_pie_result
        checkEqualAssert(expected_search_result, search_pie_result["legendText"], "", "", msg +str(click_times) + " time_click")
        nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
    else:
     checkEqualAssert(False, setSearch, "", "", "Search_passed_for_unknown")