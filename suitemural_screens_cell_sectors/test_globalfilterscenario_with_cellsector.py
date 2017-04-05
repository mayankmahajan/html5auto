from MuralUtils import Helper
from MuralUtils.AccessTechnologyHelper import *
from classes.Pages.GlobalFiltersPopClass import *
from classes.Pages.MuralScreens.CellSectorClass import *

try:
    for i in range(29):
        setup = SetUp()
        sleep(8)
        login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
        wfstart = WorkflowStartComponentClass()
        sleep(8)
        wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
        networkScreenInstance = NetworkScreenClass(setup.d)
        networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        networkScreenInstance.cm.goto("Cell Sectors", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)

        globalFilterInstance = GlobalFiltersPopClass(setup.d)
        cellsectorScreenInstance = CellSectorClass(setup.d)

        screenName = cellsectorScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.CellSectorScreen, "exploreBar"))

        logger.info("Going to %s", str(screenName))

        Helper.clickOnfilterIcon(setup,MuralConstants.CellSectorScreen)
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
            validateIncompatibleFilter(setup, Msg, MuralConstants.CellSectorScreen)
        else:
            # get global filter from Screen
            globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.CellSectorScreen,
                                                                       globalFilterInstance, setup)
            # popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)
            checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for " + screenName)

            tableHandle = getHandle(setup, MuralConstants.CellSectorScreen, "table")

            data = cellsectorScreenInstance.table.getTableData1(tableHandle, "table",length=5)
            #tableMap = cellsectorScreenInstance.table.getTableDataMap(tableHandle, driver=setup, colIndex=-1)

            if data['rows'] == Constants.NODATA:
                logger.info("No Table Data for globalfilter=%s ",globalFilterFromScreen )

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.info("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()