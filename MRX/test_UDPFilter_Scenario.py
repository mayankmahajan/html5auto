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
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    actualAvailableQuickLinkList=UDHelper.availableQuickLink(setup,MRXConstants.UDPPOPUP)
    checkEqualAssert(MRXConstants.ExpectedQuickLinkList,actualAvailableQuickLinkList,message='Verify that a user is able to select filter time range as "Last 30 days", "Last 7 Days", "Yesterday", "Last 24 Hours", "Last 4 Hours"," Today" or, from calendar',testcase_id='MKR-1762')

    actualAvailableMeasureList=UDHelper.availableMeasure(setup,MRXConstants.UDPPOPUP,index=0)
    checkEqualAssert(MRXConstants.ExpectedMeasure,actualAvailableMeasureList,message='Verify that a user is able to select Measure as "Volume (Upload)", "Volume (Download)", "Volume", # Session',testcase_id='MKR-1763')

    udpHandle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    availableFilter.append(str(udpHandle['availablefilter']['option'][0].text))
    availableFilter.append(str(udpHandle['availablefilter']['option'][1].text))

    for dim in udpHandle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that on clicking Filter icon User Distribution Parameters window appears with all the possible fields on which filter can be applied",testcase_id='MKR-1759')


    expected = {}
    expected = UDHelper.setGlobalFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER,udpFilterFromScreen, message="Verify that on pressing Cancel button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')


    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    expected = {}
    expected = UDHelper.setGlobalFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickIcon(getHandle(setup, MRXConstants.UDPPOPUP,'icons'),child='closePopupIcon')
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing X button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')

    setup.d.close()

    ###################################### Filter Scenario #############################################################

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
        checkEqualDict(popUpTooltipData, screenTooltipData,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied", doSortingBeforeCheck=True,testcase_id='MKR-1760')

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
