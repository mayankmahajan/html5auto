# This Script tests Delete,DeleteAll,Acknowledge Functionalities

from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
setup=SetUp()

login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
isError(setup)
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"ALERTS")
isError(setup)

deleteAllAlert(setup,1,False)
deleteAlert(setup,1,False)


deleteAlert(setup,1,True)
deleteAllAlert(setup,1,True)

setup.d.close()

# createKPIAlert(setup)
# GUIDE_INFO
# setup.d.close()