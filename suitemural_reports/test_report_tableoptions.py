from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *
from Utils.utility import *

setup = SetUp()
sleep(15)
login(setup, "admin", "admin123")


# print isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")

# print isError(setup)



# print ReportsHelper.getFiltersInfo(setup, 2)
print ReportsHelper.downloadReport(setup, 3)
print ReportsHelper.deleteReport(setup, 5)


# Closing the browser
setup.d.close()