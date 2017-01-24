import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.QuickTrendsPageClass import *

setup = SetUp()
login(setup, "admin", "Admin@123")
launchPage(setup,"nf_Screen")
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,"nf_Screen")



########################################################################

nfScreenInstance.cm.activateContextMenuOptions(nfScreenHandle)
nfScreenInstance.cm.launchTrends(nfScreenHandle)

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")
list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)



t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)
# Closing the Testcase
setup.d.close()