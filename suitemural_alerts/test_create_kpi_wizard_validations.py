from Utils.SetUp import *
from MuralUtils import AlertsHelper
from Utils.utility import *
try:
    setup=SetUp()
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

    print isError(setup)

    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup,"explore_Screen")
    exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")

    print isError(setup)

    AlertsHelper.validateKPIAlertWizard(setup)

    # GUIDE_INFO
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e

