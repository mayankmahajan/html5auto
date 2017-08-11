from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
from classes.Pages.TrendingMonitoringPageClass import *
import copy

import sys
try:
    setup = SetUp()
    sleep(4)
    login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    sleep(4)
    wfstart.launchScreen("Trend", getHandle(setup, MuralConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    h = getHandle(setup, MuralConstants.TMSCREEN, 'trend-slider')
    TMScreenInstance.quicktrends.clickOnExpandButton(h, setup=setup)
    globalFilterInstance = GlobalFiltersPopClass(setup.d)


    #click on filterIcon
    Helper.clickOnfilterIcon(setup,MuralConstants.CellSectorScreen)
    Helper.setGlobalFilters(globalFilterInstance, setup)
    globalFilterInstance.clickButton("Clear All", getHandle(setup, MuralConstants.GFPOPUP, MuralConstants.ALLBUTTONS))
    selectedfilter = globalFilterInstance.getAllSelectedFilters(getHandle(setup, MuralConstants.GFPOPUP))
    checkEqualAssert("No filters",str(selectedfilter),"","","Verify clear all option for global filter")


    expected={}
    #set global filter and return expected filter
    expected = Helper.setGlobalFilters(globalFilterInstance, setup)
    # get global filter from PopUpToolTipScreen
    popUpTooltipData = Helper.getGlobalFiltersToolTipData(MuralConstants.GFPOPUP, globalFilterInstance, setup)
    checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections")

    # apply global filters

    globalFilterInstance.clickButton("Apply", getHandle(setup, MuralConstants.GFPOPUP, MuralConstants.ALLBUTTONS))
    isError(setup)
    Flag,Msg=isInvalidFilter(setup)
    if Flag==True:
        validateIncompatibleFilter(setup,Msg,MuralConstants.ContentScreen)
    else:
        # get global filter from Screen
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.TMSCREEN, globalFilterInstance, setup)
        checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for Trending and Monitoring")
        TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.TableViewIndex, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
        data = TMScreenInstance.table.getTableDataMap(getHandle(setup, MuralConstants.TMSCREEN, "table"), driver=setup)

        if data['rows'] == 'No Data':
            logger.info("No Data for globalfilter=%s ", globalFilterFromScreen)
            raise

        globalFilterInstance.clearGlobalFilters(getHandle(setup, MuralConstants.TMSCREEN, "filterArea"))
        isError(setup)
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.TMSCREEN, globalFilterInstance, setup)
        checkEqualAssert("No filters", globalFilterFromScreen, "", "", "Verify clear Global Filter on T and M screen ")

    TMScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.TMSCREEN))
    TMScreenInstance.cm.gotoScreenViaWorkFlowDrop('MURAL Network Insights',getHandle(setup, MuralConstants.TMSCREEN))
    isError(setup)

    screenName = TMScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    checkEqualAssert('Network Topology',screenName,message='Network Insight launch successfully from Trendng and Monitoring via workflow')

    TMScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.NWSCREEN))
    TMScreenInstance.cm.gotoScreenViaWorkFlowDrop('Trending & Monitoring',getHandle(setup, MuralConstants.NWSCREEN))
    isError(setup)


    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.info("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()