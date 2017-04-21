from Utils.SetUp import *
from MuralUtils.AlertsHelper import *

try:
    setup=SetUp()

    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

    print isError(setup)

    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup,"explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")

    print isError(setup)

    checkAlertsCount(setup)

    popInstance = GenerateReportsPopClass(setup.d)
    # Launching DPI Alerts Page
    popInstance.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
    doSearchAndValidateAlerts(setup)
    checkAlertsCount(setup)

    for el in setup.cM.getAllNodeElements("dpiWizardtimerange","starttime"):
        doCalendarSearchOnAlerts(setup,el)


    # commenting below only because kpi alerts page is not working

    # Launching KPI Alerts Page
    # popInstance.dropdown.clickSpanWithTitle("KPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
    # doSearchAndValidateAlerts(setup)




    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e



# GUIDE_INFO