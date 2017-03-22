from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *
from suitemural_screens.test_accesstechnology_general import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
import copy

import sys


def setAndGetPieLegend(screenInstance,driverHelper,indices,handlrs,force=False):
    screenInstance.pielegend.setSelection(driverHelper, [indices],handlrs, force)
    r =screenInstance.pielegend.getData11(handlrs)
    value= str(r['legendText'][indices].split('\n')[0]).split()
    return value

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
    login(setup,"admin","Admin@123")
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
    networkScreenInstance = NetworkScreenClass(setup.d)
    #networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    #networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    globalFilterInstance = GlobalFiltersPopClass(setup.d)
    #accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    logger.info("Going to %s", str(screenName))

    #click on filterIcon
    Helper.clickOnfilterIcon(setup,MuralConstants.NWSCREEN)

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
    globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.NWSCREEN, globalFilterInstance, setup)
    #popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)

    checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for "+screenName)

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    logger.info("Going to %s",str(screenName))


    # for Testing global filter across screen

    Helper.clickOnfilterIcon(setup, MuralConstants.ATSCREEN)
    Helper.setGlobalFilters(globalFilterInstance, setup,'1')
    globalFilterInstance.clickButton("Apply", getHandle(setup, MuralConstants.GFPOPUP, MuralConstants.ALLBUTTONS))
    isError(setup)

    accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb("MURAL Network Insights",getHandle(setup, MuralConstants.ATSCREEN, "breadcrumb"))
    isError(setup)
    screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    logger.info("Going to %s", str(screenName))

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    isError(setup)
    screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    logger.info("Going to %s", str(screenName))


    #set and get main chart (pielegend) for global filter
    value = []
    value.append(setAndGetPieLegend(accesstechnologyScreenInstance,setup.dH,0,getHandle(setup, MuralConstants.ATSCREEN, "pielegend"),True))

    previousGFs,updatedGFs = updateGlobalFilters(setup,MuralConstants.ATSCREEN,expected,value)

    logger.info("Global Filter value on Access Screen before the main chart selection (pielegend) on access screen  = %s", previousGFs)
    logger.info("Global Filter value on Access Screen after the main chart selection (pielegend) on access screen = %s", updatedGFs)


    accesstechnologyScreenInstance.cm.activate(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    accesstechnologyScreenInstance.cm.goto("Devices", getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))


    screenInfo = setup.cM.getNodeElements("screenDetails", "screen")

    #accesstechnologyScreenInstance.cm.activate(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"), child="export")
    #accesstechnologyScreenInstance.cm.goto(str(screenInfo[MuralConstants.TandMScreen]['breadcrumbTitle']),getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

    #globalFilterFromScreen_TAM = Helper.getGlobalFiltersFromScreen(MuralConstants.TandMScreen, globalFilterInstance, setup)

    globalFilterFromScreen_Device = Helper.getGlobalFiltersFromScreen(MuralConstants.DeviceScreen, globalFilterInstance,setup)

    checkEqualDict(updatedGFs,globalFilterFromScreen_Device, "", "", "Verify Global Filter across Screen")


    screenNamefrombreadcrumb = str(screenInfo[MuralConstants.ATSCREEN]['breadcrumbTitle'])

    accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb(screenNamefrombreadcrumb, getHandle(setup, MuralConstants.ATSCREEN, "breadcrumb"))
    globalFilterFromPreviousScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.ATSCREEN, globalFilterInstance,setup)

    checkEqualDict(previousGFs,globalFilterFromPreviousScreen,"","","Verify Global filter on previous screen "+screenNamefrombreadcrumb)
    setup.d.close()

except Exception as e:
    raise e
    print str(e)
    # sys._current_frames()
    setup.d.close()