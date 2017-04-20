from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
setup=SetUp()
login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")


checkDPIAlerts(setup)
setup.d.close()

# createKPIAlert(setup)
# GUIDE_INFO
# setup.d.close()