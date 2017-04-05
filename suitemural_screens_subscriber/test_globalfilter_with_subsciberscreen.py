from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.SubscriberClass import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
import copy

import sys



def updateGlobalFilters(setup,screenName,expected,value):
    temp = deepcopy(expected)
    screenInfo = setup.cM.getNodeElements("screenDetails", "screen")
    dimArray = str(screenInfo[screenName]['dimensions']).split(',')
    for i in range(len(value)):
        expected[dimArray[i]] = value[i]
    return temp,expected

try:


    setup = SetUp()
    sleep(8)
    login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network", getHandle(setup, MuralConstants.WFSTARTSCREEN))
    networkScreenInstance = NetworkScreenClass(setup.d)
    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Top Subscribers", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    subscriberScreenInstance = SubscriberScreenClass(setup.d)

    globalFilterInstance = GlobalFiltersPopClass(setup.d)
    #accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.SubscriberScreen, "exploreBar"))
    logger.info("Going to %s", str(screenName))

    #click on filterIcon
    Helper.clickOnfilterIcon(setup,MuralConstants.SubscriberScreen)
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

    Flag, Msg = isInvalidFilter(setup)
    if Flag == True:
        validateIncompatibleFilter(setup, Msg, MuralConstants.SubscriberScreen)
    else:
        # get global filter from Screen
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.CellSectorScreen,globalFilterInstance, setup)
        # popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)
        checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for " + screenName)

        tableHandle = getHandle(setup, MuralConstants.SubscriberScreen, "table")

        data = subscriberScreenInstance.table.getTableData1(tableHandle, "table", length=5)
        if data['rows'] == Constants.NODATA:
            logger.info("No Table Data for globalfilter=%s ", globalFilterFromScreen)
            sys.exit()

    globalFilterInstance.clearGlobalFilters(getHandle(setup,MuralConstants.SubscriberScreen,"filterArea"))
    isError(setup)
    globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.SubscriberScreen, globalFilterInstance,setup)
    checkEqualAssert("No filters", globalFilterFromScreen, "", "", "Verify clear Global Filter on screen " + screenName)

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.info("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()