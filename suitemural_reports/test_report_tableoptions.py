from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Pages.ReportsModuleClass import *

setup = SetUp()

login(setup, "admin", "admin123")

print ReportsHelper.getFiltersInfo(setup, 2)
print ReportsHelper.downloadReport(setup, 3)
print ReportsHelper.deleteReport(setup, 5)


# Closing the browser
setup.d.close()