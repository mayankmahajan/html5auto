import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NeNePageClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

screen_name='site_Screen'
# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,screen_name)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,screen_name)


# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"NA","NA","to check def selection should be one")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
#Drill to NE screen
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)


# Get the instance of the ne screen
neScreenInstance= NEPageClass(setup.d)

#get the handle of ne screen
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

#select any pielagent on ne screen
neScreenInstance.pielegend.setSelection(setup.dH,[3],neScreenHandle)

#Drill to nene screen
drilltoScreen(setup.d,setup.dH,Constants.NENE)


# Get the Instance of the nene screen
neneScreenInstance=NeNePageClass(setup.d)

# Get the handles of the nene screen
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
                   expected_search_result = btvdata["BTVCOLUMN1"]
              neneScreenHandle = getHandle(setup, Constants.NETWORKFUNCTIONS)
              search_btv_result=neneScreenInstance.btv.getData(neneScreenHandle)
              print search_btv_result
              checkEqualAssert(expected_search_result, search_btv_result["BTVCOLUMN1"], "", "", "Search_passed_for_"+str(word)+str(click_times))
    else:
         checkEqualAssert(False, setSearch, "", "", "Search_passed_for_unknown")