from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *
from suitemural_network.test_accesstechnology_general import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
import copy

import sys

try:
    for i in range(3):
        setup = SetUp()
        sleep(8)
        login(setup,"admin","Admin@123")
        wfstart = WorkflowStartComponentClass()
        sleep(8)
        wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
        networkScreenInstance = NetworkScreenClass(setup.d)
        networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)
        globalFilterInstance = GlobalFiltersPopClass(setup.d)
        accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

        screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

        logger.info("Going to %s", str(screenName))

        Helper.clickOnfilterIcon(setup,MuralConstants.ATSCREEN)
        #set global filter and return expected filter
        expected = Helper.setGlobalFilters(globalFilterInstance, setup,str(i))
        isError(setup)

        # get global filter from PopUpToolTipScreen
        popUpTooltipData = Helper.getGlobalFiltersToolTipData(MuralConstants.GFPOPUP, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections")

        # apply global filters
        globalFilterInstance.clickButton("Apply", getHandle(setup, MuralConstants.GFPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)

        # get global filter from Screen
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.NWSCREEN, globalFilterInstance, setup)
        #popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for %s",screenName)

        setup.d.close()

except Exception as e:
    raise e
    print str(e)
    # sys._current_frames()
    setup.d.close()