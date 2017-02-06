import unittest
from Utils.logger import *
from selenium import webdriver
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NFPageClass import *
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

set_measure="Checking the combination of the measure:- "+measures[0] + ","
set_time="Time :-" +quicklinks[0]+","

nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)



nfScreenInstance.pielegend.setSelection(setup.dH,[1],nfScreenHandle)
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)
deflegendSel = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
defpieSel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
test_case6="Check Selection of pieLegend at NF screen"
checkEqualAssert(str([1]),str(deflegendSel['selIndices']),set_time,set_measure,test_case6)

setup.d.close()