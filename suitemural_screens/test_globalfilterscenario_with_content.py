from MuralUtils import Helper
from MuralUtils.AccessTechnologyHelper import *
from classes.Pages.GlobalFiltersPopClass import *
from classes.Pages.MuralScreens.CellSectorClass import *

try:
    for i in range(9):
        setup = SetUp()
        sleep(8)
        login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
        wfstart = WorkflowStartComponentClass()
        sleep(8)
        wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
        networkScreenInstance = NetworkScreenClass(setup.d)
        networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        networkScreenInstance.cm.goto("Content", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)

        globalFilterInstance = GlobalFiltersPopClass(setup.d)
        screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

        logger.info("Going to %s", str(screenName))

        Helper.clickOnfilterIcon(setup,MuralConstants.NWSCREEN)
        #set global filter and return expected filter
        expected = Helper.setGlobalFilters(globalFilterInstance, setup,str(i))
        isError(setup)

        # get global filter from PopUpToolTipScreen
        popUpTooltipData = Helper.getGlobalFiltersToolTipData(MuralConstants.GFPOPUP, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections" )

        # apply global filters
        globalFilterInstance.clickButton("Apply", getHandle(setup, MuralConstants.GFPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)

        # get global filter from Screen
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.NWSCREEN, globalFilterInstance, setup)
        #popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for "+screenName)

        btvdata0 = networkScreenInstance.multibtv.getBTVData(setup,getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=0)

        if btvdata0 == False:
            logger.info("No Data for globalfilter=%s ",globalFilterFromScreen )

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()