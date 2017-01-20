import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.InterfacePageClass import *



# Getting Setup Details
setup = SetUp()


# Launching Application
login(setup, "admin", "Admin@123")


# launchPage(setup,"site_Screen")
# siteScreenInstance = SitePageClass(setup.d)
# siteScreenHandle = getHandle(setup,"site_Screen")
#
# data = siteScreenInstance.btv.getData(siteScreenHandle)
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","interface_Screen")
# Get the Instance of the screen
screenInstance = InterfacePageClass(setup.d)

# Get the handles of the screen
interfaceScreenHandle = getHandle(setup,Constants.INTERFACES)

alphabets = screenInstance.searchComp.setSearchText(interfaceScreenHandle,"alphabets")
time.sleep(2)

#text = screenInstance.searchComp.getSearchText(siteScreenHandle)

if(alphabets==True):
    screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,alphabets,"","","Search_passed_for_alphabets")
else:
    checkEqualAssert(False,alphabets,"","","Search_failed_for_alphabets")


backspace = screenInstance.searchComp.setSearchText(interfaceScreenHandle,Keys.BACK_SPACE)
sleep(2)

if(backspace==True):
    screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,backspace,"","","Search_passed_for_backspace_button")
else:
    checkEqualAssert(False,backspace,"","","Search_failed_for_backspace_button")


cross = screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
if(cross==None):
    screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
    time.sleep(10)
    checkEqualAssert(None,cross,"","","Search_passed_for_cross_button")
else:
    checkEqualAssert(False,cross,"","","Search_failed_for_cross_button")


numeric = screenInstance.searchComp.setSearchText(interfaceScreenHandle,"0123456789")
time.sleep(2)

if(numeric==True):
    screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,alphabets,"","","Search_passed_for_numeric")
else:
    checkEqualAssert(False,alphabets,"","","Search_failed_for_numeric")

screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)

special_characters = screenInstance.searchComp.setSearchText(interfaceScreenHandle,"!@#$%^&*()_+=?/><.,")
time.sleep(2)

if(special_characters==True):
    screenInstance.searchComp.hitSearchIcon(interfaceScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,special_characters,"","","Search_passed_for_special_characters")
else:
    checkEqualAssert(False,special_characters,"","","Search_failed_for_characters")

# Logging out of the application
setup.d.close()
