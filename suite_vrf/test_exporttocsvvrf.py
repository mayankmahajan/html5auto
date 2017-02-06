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

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")
# Get the Instance and handle of the screen
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")


# Get the default selection

screenInstance.btv.setSelection(2,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.VRF)

vrfScreenInstance = VrfPageClass(setup.d)
vrfScreenHandle = getHandle(setup,Constants.VRF)

# Set the bar Table view to the 2 index
vrfScreenInstance.btv.setSelection(2,vrfScreenHandle)

result = exportTo(setup,setup.dH,'EXPORTTOCSV')

checkEqualAssert(result,True,"","","Checking the functionality of the EXPORT TO CSV at Vrf Screen")

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
