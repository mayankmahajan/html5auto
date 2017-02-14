from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *
from MuralUtils.MuralConstants import *
from Utils.utility import *

setup = SetUp()
# sleep(120)
login(setup, "admin", "admin123")

# print isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")

# print isError(setup)



setup.d.save_screenshot('../screenshots/screenie.png')

tableMap = ReportsHelper.getTableDataMap(setup,MuralConstants.REPORTSCREEN)

columnName = "Name"
sortedData = ReportsHelper.sortTable(setup, columnName)

resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
checkEqualDict(sortedData,tableMap['rows'],"","","Checking each row")

# Closing the browser
setup.d.close()