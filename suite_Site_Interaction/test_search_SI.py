import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

# Logging into the appliction
login(setup, "admin", "Admin@123")

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

alphabets = screenInstance.searchComp.setSearchText(siteScreenHandle,"alphabets")
time.sleep(2)

#text = screenInstance.searchComp.getSearchText(siteScreenHandle)

if(alphabets==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,alphabets,"","","Search_passed_for_alphabets")
else:
    checkEqualAssert(False,alphabets,"","","Search_failed_for_alphabets")


backspace = screenInstance.searchComp.setSearchText(siteScreenHandle,Keys.BACK_SPACE)
sleep(2)

if(backspace==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,backspace,"","","Search_passed_for_backspace_button")
else:
    checkEqualAssert(False,backspace,"","","Search_failed_for_backspace_button")


cross = screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
if(cross==None):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(str(None),cross,"","","Search_passed_for_cross_button")
else:
    checkEqualAssert(False,cross,"","","Search_failed_for_cross_button")


numeric = screenInstance.searchComp.setSearchText(siteScreenHandle,"0123456789")
time.sleep(2)

if(numeric==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,alphabets,"","","Search_passed_for_numeric")
else:
    checkEqualAssert(False,alphabets,"","","Search_failed_for_numeric")

screenInstance.searchComp.hitSearchIcon(siteScreenHandle)

special_characters = screenInstance.searchComp.setSearchText(siteScreenHandle,"!@#$%^&*()_+=?/><.,")
time.sleep(2)

if(special_characters==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,special_characters,"","","Search_passed_for_special_characters")
else:
    checkEqualAssert(False,special_characters,"","","Search_failed_for_characters")

# Logging out of the application
setup.d.close()

