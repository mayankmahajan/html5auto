from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
from classes.Pages.TrendingMonitoringPageClass import *
import copy

try:
    for i in range(29):
        setup = SetUp()
        login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
        wfstart = WorkflowStartComponentClass()
        wfstart.launchScreen("Trend", getHandle(setup, MuralConstants.WFSTARTSCREEN))
        TMScreenInstance = TrendingMonitoringPageClass(setup.d)
        h = getHandle(setup, MuralConstants.TMSCREEN, 'trend-slider')
        TMScreenInstance.quicktrends.clickOnExpandButton(h, setup=setup)
        globalFilterInstance = GlobalFiltersPopClass(setup.d)

        Helper.clickOnfilterIcon(setup,MuralConstants.TMSCREEN)
        #set global filter and return expected filter
        expected = Helper.setGlobalFilters(globalFilterInstance, setup,str(i))
        isError(setup)

        # get global filter from PopUpToolTipScreen
        popUpTooltipData = Helper.getGlobalFiltersToolTipData(MuralConstants.GFPOPUP, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections" )

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
            checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for Trending and Monitoring")

            tableHandle = getHandle(setup, MuralConstants.SubscriberScreen, "table")

            data = TMScreenInstance.table.getTableData1(tableHandle, "table", length=5)
            if data['rows'] == Constants.NODATA:
                r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                setup.d.save_screenshot(r)
                logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved", globalFilterFromScreen,r)
                resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved", globalFilterFromScreen,r)
        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.info("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()