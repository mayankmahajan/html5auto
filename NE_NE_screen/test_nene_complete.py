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
print set_time
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")
setTimeRange(setup,set_time)
a=screenInstance.measure.doSelection(siteScreenHandle,set_measure)
print a



# screenInstance = SitePageClass(setup.d)
# setTimeRange(setup,set_time)
# a=screenInstance.measure.doSelection(siteScreenHandle,set_measure)
# setMeasure(setup,set_measure,"site_Screen")
# siteScreenHandle = getHandle(setup,"site_Screen")
# #######################################################################

#######################################################################
# Get the default selection and Validate the result
siteScreenHandle =getHandle(setup,"site_Screen")
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
test_case9="New Selection in table"
checkEqualAssert("Table",str(VAR),set_time,set_measure,test_case9)
#######################################################################

#Check single and multiple selection
neneScreenInstance.switcher.setSelection(0,neneScreenHandle)
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
        screenInstance.measure.doSelection(neneScreenHandle, measures[i])

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
data1=neneScreenInstance.btv.getData(neneScreenHandle)
print data1

# text=["r","s","-","$","!","@","#","%","^","&","*","()","+","=","",Keys.BACK_SPACE]
text=["r","ss",Keys.BACK_SPACE]
# Search testing. Length of text list should be >=2 if we have to check backspace key functionality.
click=["one","two"]
count=1
for word in text:
    if word==Keys.BACK_SPACE:
       index_previous=text.index(Keys.BACK_SPACE)-1
       word1=text[text.index(Keys.BACK_SPACE)-1][:-1]
       setSearch = neneScreenInstance.searchComp.setSearchText(neneScreenHandle, text[index_previous])
       msg="Search_for_Backspace "

    else:
        word1=word
        msg="Search_for_"+word+" "
    expected_search_result=[data1["BTVCOLUMN1"][i] for i in range(2,len(data1["BTVCOLUMN1"])) if data1["BTVCOLUMN1"][i].lower().find(word1.lower()) >= 0]
    print word1,expected_search_result
    setSearch = neneScreenInstance.searchComp.setSearchText(neneScreenHandle,word)
    time.sleep(5)
    if(setSearch==True):
     for click_times in click:
        if click_times == "one":
            #single hit on search button
            neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
        elif click_times == "two" and count==1:
            #bouble hit on search button
            neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
            neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
            expected_search_result = data1["BTVCOLUMN1"][2::]
            count=0
        else:
            break
        neneScreenHandle = getHandle(setup, Constants.NENE)
        search_pie_result=neneScreenInstance.btv.getData(neneScreenHandle)
        print search_pie_result
        checkEqualAssert(expected_search_result,search_pie_result["BTVCOLUMN1"][2::], "", "", msg+str(click_times)+" time click")
        neneScreenInstance.searchComp.hitSearchIcon(neneScreenHandle)
    else:
     checkEqualAssert(False,setSearch, "", "", "Search_for_unknown")