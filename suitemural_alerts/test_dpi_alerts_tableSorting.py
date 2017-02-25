from MuralUtils import AlertsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *
from MuralUtils.MuralConstants import *
from Utils.utility import *

setup = SetUp()
sleep(6)
login(setup, "admin", "admin123")

print isError(setup)

popInstance = GenerateReportsPopClass(setup.d)
# Launching Settings Page
popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
popInstance.switcher.switchTo(0,getHandle(setup,MuralConstants.ALERTSCREEN,"settings"),"settings")

print isError(setup)

tableMap = AlertsHelper.getTableDataMap(setup,MuralConstants.REPORTSCREEN)

# columnName = "Name"
columns = ["DPI Alert Rule Name","Frequency","Measure","Range","Status"]
for columnName in columns:
    sortedData = AlertsHelper.sortTable(setup, columnName)

    resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
    checkEqualDict(sortedData,tableMap['rows'],"","","Checking each row of DPI Alerts Table")

# Closing the browser
setup.d.close()