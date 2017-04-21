from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *
from MuralUtils.MuralConstants import *
from Utils.utility import *

try:
    setup = SetUp()
    # sleep(15)
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

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

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e

