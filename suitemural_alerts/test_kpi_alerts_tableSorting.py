from MuralUtils import AlertsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *
from MuralUtils.MuralConstants import *
from Utils.utility import *

try:
    setup = SetUp()
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

    print isError(setup)

    popInstance = GenerateReportsPopClass(setup.d)
    # Launching Settings Page
    popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
    popInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.ALERTSCREEN,"settings"),"settings")

    print isError(setup)

    tableMap = AlertsHelper.getTableDataMap(setup,MuralConstants.REPORTSCREEN)

    # columnName = "Name"
    columns = ["KPI Alert Rule Name","Schema","KPI","Index","Status"]
    for columnName in columns:
        sortedData = AlertsHelper.sortTable(setup, columnName)

        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
        checkEqualDict(sortedData,tableMap['rows'],"","","Checking each row of KPI Alerts Table")

    # Closing the browser
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e


