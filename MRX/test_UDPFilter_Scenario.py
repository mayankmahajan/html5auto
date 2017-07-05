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

    UDHelper.setQuickLink_Measure(setup, udScreenInstance, str('testCalender')) # Check Calender Scenario (Start Time > End Time)
    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER,udpFilterFromScreen, message="Verify that on pressing Cancel button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')


    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickIcon(getHandle(setup, MRXConstants.UDPPOPUP,'icons'),child='closePopupIcon')
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing X button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')

    ############################################## For Toggle State ########################################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    expectedtoggleState = {}
    expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_NotEqual',toggleStateFlag=True)
    isError(setup)
    click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    if click_Status:
        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
        actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_NotEqual',validateSearch=True)
        isError(setup)
        checkEqualDict(expectedtoggleState,actualtoggleState,message='Verify that toggle button should have that same state that you set while applying filters (Select All + Not Equal)',testcase_id='MKR-3095')
        udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))


    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    expectedtoggleState = {}
    expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_Equal',toggleStateFlag=True)
    isError(setup)
    click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    if click_Status:
        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
        actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_Equal')
        isError(setup)
        checkEqualDict(expectedtoggleState,actualtoggleState,message='Verify that toggle button should have that same state that you set while applying filters (Select All + Equal)',testcase_id='MKR-3095')
        udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    ####################################################################################################################

    setup.d.close()


    ###################################### Filter Scenario #############################################################

    for i in range(0,6):
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
        expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(i))
        isError(setup)
        popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)
        for k in MRXConstants.ListOfFilterContainingTree:
            if expected[k]!=[]:
                checkEqualAssert(expected[k],popUpTooltipData[k],message='Verify Tree selection on UI ( it should be like level 1 > level 2 > level 3 and soon',testcase_id='MKR-3198')
        checkEqualDict(expected,popUpTooltipData,message="Verify Filters Selections",doSortingBeforeCheck=True)

        # apply global filters
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)

        h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
        timeRangeFromScreen=str(h['time_measure']['span'][0].text).strip()
        measureFromScreen=str(h['time_measure']['span'][1].text).strip()
        checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,message='After apply filter verify timerange value on screen')
        checkEqualAssert(measureFromPopup,measureFromScreen,message='After apply filter verify measure value on screen')
        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
        checkEqualDict(expected, screenTooltipData,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied", doSortingBeforeCheck=True,testcase_id='MKR-1760')

        tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
        data = udScreenInstance.table.getTableData1(tableHandle, "table", length=5)
        if data['rows'] == Constants.NODATA:
            h=getHandle(setup, MRXConstants.UDSCREEN, "table")['table']['no_data_msg']
            if len(h)>0:
                msg=str(h[0].text)
                checkEqualAssert(MRXConstants.NODATAMSG,msg,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
            else:
                checkEqualAssert(MRXConstants.NODATAMSG,'',measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
            resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    #raise e
    setup.d.close()
