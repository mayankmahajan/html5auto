from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
import os
from classes.Objects.Report import *
from classes.Objects.Time import *
from Utils import ReportsHelper

setup = SetUp()

login(setup, "admin", "admin123")

tableMap = ReportsHelper.getTableDataMap(setup)

columnName = "Name"
sortedData = ReportsHelper.sortTable(setup,columnName)

resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
checkEqualDict(sortedData,tableMap['rows'],"","","Checking each row")

# Closing the browser
setup.d.close()