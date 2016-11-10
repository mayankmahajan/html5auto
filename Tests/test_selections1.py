import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *


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
launchPage(setup,"nf_Screen")

# GetScreenInstance and control over its Components
nfScreenInstance = NFPageClass(setup.d)
nfScreenHandle = getHandle(setup,"nf_Screen")

# GetSelection
defaultSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)

# Log Result
checkEqualAssert([0],defaultSelection['selIndices'],"NA","NA","Default Selection at NFScreen")

# SetSelection
nfScreenInstance.pielegend.setSelection(setup.dH,[3],nfScreenHandle)
nfScreenHandle = getHandle(setup,"nf_Screen")
nfScreenInstance.pielegend.setSelection(setup.dH,[6],nfScreenHandle)
nfScreenHandle = getHandle(setup,"nf_Screen")

# GetSelection
updatedSelection = nfScreenInstance.pielegend.getSelection(nfScreenHandle)

# Log Result
checkEqualAssert([1,3,6],updatedSelection['selIndices'],"NA","NA","Updated Selection at NFScreen")

# Check PieWedge Expanded
pieSelections = nfScreenInstance.pie.getPieSelections(nfScreenHandle)

# GetChartData
piedata = nfScreenInstance.pielegend.getData(nfScreenHandle)
# GetTooltipData
piedata['tooltipdata'] = nfScreenInstance.pie.getToolTipInfo(setup.d,setup.dH,nfScreenHandle)

# nfScreenInstance.pielegend.validateBTVData()

# Log Result
checkEqualAssert(piedata['legendText'],piedata['tooltipdata'],"NA","NA","Pie Tooltip Validations at NFScreen")


# Closing the Testcase
setup.d.close()