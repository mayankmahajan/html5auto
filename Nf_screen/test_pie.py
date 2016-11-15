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

# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
#checkEqualAssert(str(1),str(defSelection['selIndex']),"","")


# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(2,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.NETWORKFUNCTIONS)


# Get the Instance of the nf screen
nfScreenInstance = NFPageClass(setup.d)

# Get the handles of the nf screenx
nfScreenHandle = getHandle(setup,Constants.NETWORKFUNCTIONS)

# Get the default selection
#deflegendSel = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
#defpieSel = nfScreenInstance.pie.getPieSelections(nfScreenHandle)

# print defnfSelection
#print defpieSel
#print deflegendSel

# Validating the result
#checkEqualAssert(str(1),str(defpieSel['selIndex']),"","")
#checkEqualAssert(str("[]"),str(deflegendSel['selIndices']),"","")




#checkEqualAssert("True",result,"","","drillToNF")
#nfScreenInstance.pie.setSelection(2,nfScreenHandle)

lenth=len(nfScreenHandle)
print lenth
l=0
while l < lenth:
    nfScreenInstance.pielegend.setSelection(setup.dH, [l], nfScreenHandle)
    pieSelections = nfScreenInstance.pie.getPieSelections(nfScreenHandle)
    updatedSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
    checkEqualAssert([l],updatedSelection['selIndices'],"NA","NA","Updated Selection at NFScreen")
    checkEqualAssert([l],pieSelections['selIndices'],"NA","NA","Updated Selection at NFScreen")
    checkEqualAssert(updatedSelection['selIndices'],pieSelections['selIndices'],"NA","NA","Updated Selection at NFScreen")

#nfScreenInstance.pielegend.setSelection(setup.dH,[0],nfScreenHandle)
#nfScreenInstance.pielegend.setSelection(setup.dH,[1],nfScreenHandle)

#updatedSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)
#pieSelections = nfScreenInstance.pie.getPieSelections(nfScreenHandle)

#print updatedSelection
#print pieSelections
#checkEqualAssert([0],updatedSelection['selIndices'],"NA","NA","Updated Selection at NFScreen")
#checkEqualAssert([1],updatedSelection['selIndices'],"NA","NA","Updated Selection at NFScreen")

