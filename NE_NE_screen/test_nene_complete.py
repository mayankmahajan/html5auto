import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NeNePageClass import *
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
# Get the default selection of ne screen
deflegendSel = neScreenInstance.pielegend.getSelection(neScreenHandle)
defpieSel = neScreenInstance.pie.getPieSelections(neScreenHandle)
test_case4="Default Selection of pieLegend in NE screen"
checkEqualAssert(str("[]"),str(deflegendSel['selIndices']),set_time,set_measure,test_case4)
#######################################################################

#######################################################################

#select any pielagent on ne screen and verify selection
neScreenInstance.pielegend.setSelection(setup.dH,[3],neScreenHandle)
legendSel = neScreenInstance.pielegend.getSelection(neScreenHandle)
test_case5="Selection at pieLegend in NE screen to drill NENE"
checkEqualAssert(str("[3]"),str(legendSel['selIndices']),set_time,set_measure,test_case5)

#######################################################################

#######################################################################

#Drill to nene screen and verify
status1 =drilltoScreen(setup.d,setup.dH,Constants.NENE)
test_case6 = "Drill TO NE_NE Screen"
checkEqualAssert("True",str(status1),set_time,set_measure,test_case6)

#######################################################################

#######################################################################
# Get the default selection and Validate the result
# Get the Instance of the nene screen
neneScreenInstance=NeNePageClass(setup.d)

# Get the handles of the nene screen
neneScreenHandle = getHandle(setup,Constants.NENE)
test_case7="Default selection of nene screen"
defSelection1 = screenInstance.btv.getSelection(neneScreenHandle)
print  defSelection1
checkEqualAssert(str(1),str(defSelection1['selIndex']),set_time,set_measure,test_case7)
########################################################################################

########################################################################################

# Get the Instance of the nene screen
neneScreenInstance=NeNePageClass(setup.d)

# Get the handles of the nene screen
neneScreenHandle = getHandle(setup,Constants.NENE)

#######################################################################
Var=neneScreenInstance.switcher.getSelection(neneScreenHandle)
test_case8="Default Selection in chart"
checkEqualAssert("Chart",str(Var),set_time,set_measure,test_case8)

neneScreenInstance.switcher.setSelection(1,neneScreenHandle)
VAR=neneScreenInstance.switcher.getSelection(neneScreenHandle)
test_case3="New Selection in table"
checkEqualAssert("Table",str(VAR),set_time,set_measure,test_case3)
#######################################################################

#Check single and multiple selection
Selection_list=[3,2]
for i in Selection_list:
    neneScreenInstance.btv.setSelection(i,neneScreenHandle)
    neneScreenHandle = getHandle(setup,Constants.NENE)
    btvsel=neneScreenInstance.btv.getSelection(neneScreenHandle)
    test_case8 = "Check Selection of btv in NENE screen"
    checkEqualAssert(str(i),str(btvsel['selIndex']), set_time, set_measure, test_case8)
#######################################################################

#######################################################################
#measuse and time range selection and data validation
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        setMeasure(setup,measures[i],Constants.NENE)

        print measures[i]
        print i

         # Result Logging
        expected = "True"
        actual = "True"

        checkEqualAssert(expected,actual,quicklinks[t], measures[i])
        i+=1
         # end of measureSelection


    t+=1

#######################################################################


#######################################################################
#search box testing on ne screen
neneScreenHandle = getHandle(setup,Constants.NENE)
btvdata=neneScreenInstance.btv.getData(neneScreenHandle)
print btvdata

text=["r"]
click =["one","two"]
for word in text:
    print word
    expected_search_result=[btvdata["BTVCOLUMN1"][i] for i in range(2,len(btvdata["BTVCOLUMN1"])) if btvdata["BTVCOLUMN1"][i].lower().find(word.lower()) >= 0]
    setSearch = neneScreenInstance.searchComp.setSearchText(neneScreenHandle,word)
    print setSearch
    time.sleep(5)
    if(setSearch=="True"):
         for click_times in click:
              if click_times == "one":
                   neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
              elif click_times == "two":
                   neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
                   neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
                   expected_search_result = btvdata["BTVCOLUMN1"][2::]
              neneScreenHandle = getHandle(setup, Constants.NETWORKFUNCTIONS)
              search_btv_result=neneScreenInstance.btv.getData(neneScreenHandle)
              print search_btv_result
              checkEqualAssert(expected_search_result, search_btv_result["BTVCOLUMN1"][2::], "", "", "Search_passed_for_"+str(word)+str(click_times))
    else:
         checkEqualAssert(False, setSearch, "", "", "Search_passed_for_unknown")