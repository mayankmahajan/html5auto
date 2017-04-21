from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
from classes.Objects.CreateAlert import *

try:
    setup=SetUp()
    sleep(6)
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
    isError(setup)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup,"explore_Screen")

    # Alerts Module
    ###################################
    exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")

    isError(setup)

    createKPIAlert(setup)
    # GUIDE_INFO
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e

