from Utils.SetUp import *
from MuralUtils import AlertsHelper
from Utils.utility import *
from classes.Objects.CreateAlert import *

setup=SetUp()
sleep(6)
login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
x =CreateAlert()

print isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")

print isError(setup)


AlertsHelper.validateDPIAlertWizard(setup,x.dict)

# GUIDE_INFO
setup.d.close()
