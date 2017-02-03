from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
import os
from classes.Objects.Report import *
from classes.Objects.Time import *
from Utils import ReportsHelper

setup = SetUp()

login(setup, "admin", "admin123")

print ReportsHelper.getFiltersInfo(setup,2)
print ReportsHelper.downloadReport(setup,3)
print ReportsHelper.deleteReport(setup,5)


# Closing the browser
setup.d.close()