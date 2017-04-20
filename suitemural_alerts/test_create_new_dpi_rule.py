from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
from classes.Objects.CreateAlert import *


setup=SetUp()
login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# Alerts Module
###################################
exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")
isError(setup)

for i in range(15):
    x = CreateAlert()
    print createDPIAlert(setup, x.dict)

# GUIDE_INFO

setup.d.close()
