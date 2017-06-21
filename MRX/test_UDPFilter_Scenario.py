import unittest
from Utils.logger import *
from selenium import webdriver
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import os

# newFilterDetails = ConfigManager().getNodeElements("savenewfilter", "filter")
# for k, filterDetail in newFilterDetails.iteritems():
#     setup = SetUp()
#     login(setup, Constants.USERNAME, Constants.PASSWORD)
#     exploreScreenInstance = ExplorePageClass(setup.d)
#     exploreHandle = getHandle(setup, "explore_Screen")
#     exploreScreenInstance.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
#     udScreenInstance = UDScreenClass(setup.d)
#     timeRangeFromPopup = ''
#     measureFromPopup = ''

try:
    for i in range(5):
        setup = SetUp()
        login(setup, Constants.USERNAME, Constants.PASSWORD)
        udScreenInstance = UDScreenClass(setup.d)
        exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
        udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
        time.sleep(3)
        udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))

        timeRangeFromPopup = ''
        measureFromPopup = ''
        UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
        SegmentHelper.clickOnfilterIcon(setup,MRXConstants.UDSCREEN,'nofilterIcon')

        timeRangeFromPopup,measureFromPopup=UDHelper.setQuickLink_Measure(setup,udScreenInstance,str(i))
        expected={}
        expected = UDHelper.setGlobalFilters(udScreenInstance, setup,str(i))
        isError(setup)
        popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)
        checkEqualDict(popUpTooltipData, expected,message="Verify Filters Selections",doSortingBeforeCheck=True)

        # apply global filters
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)

        h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
        timeRangeFromScreen=str(h['time_measure']['span'][0].text).strip()
        measureFromScreen=str(h['time_measure']['span'][1].text).strip()
        checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,message='After apply filter verify timerange value on screen')
        checkEqualAssert(measureFromPopup,measureFromScreen,message='After apply filter verify measure value on screen')
        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
        checkEqualDict(popUpTooltipData, screenTooltipData,message="Verify Filters Selections", doSortingBeforeCheck=True)

        tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
        data = udScreenInstance.table.getTableData1(tableHandle, "table", length=5)

        if data['rows'] == Constants.NODATA:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            #setup.d.save_screenshot(r)
            logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
            resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()
