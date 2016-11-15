import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *




# Getting Setup Details
setup = SetUp()


# Launching Application
login(setup, "admin", "Admin@123")


# launchPage(setup,"site_Screen")
# siteScreenInstance = SitePageClass(setup.d)
# siteScreenHandle = getHandle(setup,"site_Screen")
#
# data = siteScreenInstance.btv.getData(siteScreenHandle)

# Launch Screen
launchPage(setup,Constants.SITES)

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
if(cross==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,cross,"","","Search_passed_for_backspace_button")
else:
    checkEqualAssert(False,cross,"","","Search_failed_for_backspace_button")


if(cross==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,backspace,"","","Search_passed_for_backspace_button")
else:
    checkEqualAssert(False,backspace,"","","Search_failed_for_backspace_button")


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
