import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *

setup = SetUp()
login(setup, "admin", "Admin@123")
launchPage(setup,"nf_Screen")
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,"nf_Screen")



########################################################################


drilltoScreen(setup.d,setup.dH,Constants.SITES)





# Closing the Testcase
setup.d.close()