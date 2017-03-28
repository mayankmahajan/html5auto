from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.CellSectorClass import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
import copy

import sys




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
    networkScreenInstance.cm.goto("Cell Sectors", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    isError(setup)

    cellsectorScreenInstance = CellSectorClass(setup.d)
    globalFilterInstance = GlobalFiltersPopClass(setup.d)

    #accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.CellSectorScreen, "exploreBar"))
    logger.info("Going to %s", str(screenName))

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
    # get global filter from Screen
    globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.CellSectorScreen, globalFilterInstance, setup)
    #popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)

    checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for "+screenName)

    globalFilterInstance.clearGlobalFilters(getHandle(setup,MuralConstants.CellSectorScreen,"filterArea"))
    isError(setup)
    globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.CellSectorScreen, globalFilterInstance,setup)
    checkEqualAssert("No filters", globalFilterFromScreen, "", "", "Verify clear Global Filter on screen " + screenName)
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()