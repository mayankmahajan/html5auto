from Utils.SetUp import *
from Utils.utility import *
from classes.Pages.InterfacePageClass import *

#######################################################################
# Getting Setup Details
setup = SetUp()
#######################################################################


#######################################################################
#get time range and measures from config file
#timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
#quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0

#measureIteration = len(setup.cM.getNodeElements("measures","measure"))
#measures = setup.cM.getNodeElements("measures","measure").keys()
#######################################################################

#######################################################################
# Logging into the appliction and launch site screen
login_status=login(setup, "admin", "Admin@123")
#checkEqualAssert(True,login_status,"","","Login to NRMCA UI")
launch_status=launchPage(setup,"interface_Screen")
checkEqualAssert(True,launch_status,"","","launch site screen")
sleep(5)
screenInstance = InterfacePageClass(setup.d)
#setMeasure(setup,set_measure,"site_Screen")
interfaceScreenHandle = getHandle(setup,"interface_Screen")
interfacedata = screenInstance.table.getIterfaceTableData(interfaceScreenHandle)
print interfacedata
setup.d.close()
