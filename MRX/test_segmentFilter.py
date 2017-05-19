import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import SegmentHelper



setup = SetUp()

login(setup,Constants.USERNAME,Constants.PASSWORD)
segmentScreenInstance = SegmentScreenClass(setup.d)
segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN)

#click on Filter Icon
'''
SegmentHelper.clickOnfilterIcon(setup,MRXConstants.SEGMENTSCREEN,'nofilterIcon')
filterScreenHandle=getHandle(setup,"filter_Screen")
checkEqualAssert("Filters",str(filterScreenHandle['allspans']['span'][0].text),'','',"Verify Filter Header Text on Filter Popup")


#filterScenarios=setup.cM.getNodeElements('segmentFilter','filter')
#for k, filterScenario in filterScenarios.iteritems():

for i in range(1):
    expected = SegmentHelper.setSegmentFilter(setup,segmentScreenInstance,k=i)
    #isError(setup)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)
    popUpTooltipData = SegmentHelper.getGlobalFiltersToolTipData(MRXConstants.SEGMENTSCREEN, segmentScreenInstance, setup,flag=False)
    checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections")
'''

filterFromScreen=SegmentHelper.getGlobalFiltersFromScreen(MRXConstants.SEGMENTSCREEN, segmentScreenInstance, setup,flag=False)
SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN,'filterIcon')
expectedFromFilterPopUp = SegmentHelper.getSegmentFilter(setup, segmentScreenInstance)
checkEqualDict(filterFromScreen, expectedFromFilterPopUp, "", "", "Verify Filters Selections")

setup.d.close()
