from Utils.SetUp import *
from MuralUtils import AlertsHelper
from Utils.utility import *

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