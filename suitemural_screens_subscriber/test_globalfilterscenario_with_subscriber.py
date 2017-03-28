from MuralUtils import Helper
from MuralUtils.AccessTechnologyHelper import *
from classes.Pages.GlobalFiltersPopClass import *
from classes.Pages.MuralScreens.SubscriberClass import *

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
        networkScreenInstance.cm.goto("Top Subscribers", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)

        globalFilterInstance = GlobalFiltersPopClass(setup.d)
        subscriberScreenInstance = SubscriberScreenClass(setup.d)

        screenName = subscriberScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.SubscriberScreen, "exploreBar"))

        logger.info("Going to %s", str(screenName))

        Helper.clickOnfilterIcon(setup,MuralConstants.SubscriberScreen)
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
        globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.SubscriberScreen, globalFilterInstance, setup)
        #popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN, globalFilterInstance, setup)

        checkEqualDict(popUpTooltipData, globalFilterFromScreen, "", "", "Verify Global Filter for "+screenName)

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()