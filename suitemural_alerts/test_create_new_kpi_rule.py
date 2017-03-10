from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
from classes.Objects.CreateAlert import *
setup=SetUp()
sleep(6)
login(setup,"admin","admin123")
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