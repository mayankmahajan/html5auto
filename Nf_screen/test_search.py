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

# Launch Site Screen
launchPage(setup,"site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screenx
siteScreenHandle = getHandle(setup,"site_Screen")


# Set the bar Table view to the 2nd index

screenInstance.btv.setSelection(2,siteScreenHandle)

#Drill to Network function page
drilltoScreen(setup.d,setup.dH,Constants.NETWORKFUNCTIONS)


# Get the Instance of the nf screen
nfScreenInstance = NFPageClass(setup.d)

# Get the handles of the nf screenx
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)
piedata=nfScreenInstance.pielegend.getData(nfScreenHandle)

text=["6","s","mm","","G","hfgjghkkkhjk","","9","8","10","6","#@$%"]
click =["one","two"]
for word in text:
    expected_search_result=[piedata["legendText"][i] for i in range(0,len(piedata["legendText"])) if piedata["legendText"][i].lower().find(word.lower()) >= 0 and piedata["legendText"][i].lower().find(word.lower()) < piedata["legendText"][i].lower().find("\n")]
    setSearch = nfScreenInstance.searchComp.setSearchText(nfScreenHandle,word)
    time.sleep(5)
    if(setSearch=="True"):
         for click_times in click:
              if click_times == "one":
                   nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
              elif click_times == "two":
                   nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
                   nfScreenInstance.searchComp.hitSearchIcon(nfScreenHandle)
                   expected_search_result = piedata["legendText"]
              nfScreenHandle = getHandle(setup, Constants.NETWORKFUNCTIONS)
              search_pie_result=nfScreenInstance.pielegend.getData(nfScreenHandle)
              print search_pie_result
              checkEqualAssert(expected_search_result, search_pie_result["legendText"], "", "", "Search_check_for_"+str(word)+str(click_times))
    else:
         checkEqualAssert(False, setSearch, "", "", "Search_check_for_unknown")