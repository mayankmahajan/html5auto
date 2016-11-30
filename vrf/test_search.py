import unittest
from Utils.logger import *
from selenium import webdriver


from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.VrfPageClass import  *
from classes.Components.SwitcherComponentClass import *
# Getting Setup Details and Launching the application


######################################################
setup = SetUp()
login(setup, "admin", "Admin@123")
#####################################################


# Launch Site Screen
launchPage(setup,"site_Screen")
sleep(5)

# Get the Instance and handle of the screen
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")


# Get the default selection

a = screenInstance.btv.setSelection(2,siteScreenHandle)
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
data=screenInstance.btv.getData(siteScreenHandle)
print data
status=drilltoScreen(setup.d,setup.dH,Constants.VRF)

neScreenInstance = VrfPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.VRF)
data1 = neScreenInstance.btv.getData(neScreenHandle)

# Search testing. Length of text list should be >=2 if we have to check backspace key functionality.
text=["ca",Keys.BACK_SPACE]
click=["one","two"]
count=1
for word in text:
    if word==Keys.BACK_SPACE:
       index_previous=text.index(Keys.BACK_SPACE)-1
       word1=text[text.index(Keys.BACK_SPACE)-1][:-1]
       setSearch = neScreenInstance.searchComp.setSearchText(neScreenHandle, text[index_previous])
       msg="Search_for_Backspace "

    else:
        word1=word
        msg="Search_for_"+word+" "
    expected_search_result=[data1["BTVCOLUMN1"][i] for i in range(2,len(data1["BTVCOLUMN1"])) if data1["BTVCOLUMN1"][i].lower().find(word1.lower()) >= 0]
    print word1,expected_search_result
    setSearch = neScreenInstance.searchComp.setSearchText(neScreenHandle,word)
    time.sleep(5)
    if(setSearch==True):
     for click_times in click:
        if click_times == "one":
            #single hit on search button
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
        elif click_times == "two" and count==1:
            #bouble hit on search button
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
            neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
            expected_search_result = data1["BTVCOLUMN1"][2::]
            count=0
        else:
            break
        neScreenHandle = getHandle(setup, Constants.VRF)
        search_pie_result=neScreenInstance.btv.getData(neScreenHandle)
        print search_pie_result
        checkEqualAssert(expected_search_result, search_pie_result["BTVCOLUMN1"][2::], "", "", msg+str(click_times)+" time click")
        neScreenInstance.searchComp.hitSearchIcon(neScreenHandle)
    else:
     checkEqualAssert(False, setSearch, "", "", "Search_for_unknown")

