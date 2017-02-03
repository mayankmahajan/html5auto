from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
import os
from classes.Objects.Report import *
from classes.Objects.Time import *
from Utils import ReportsHelper

setup = SetUp()

login(setup, "admin", "admin123")

ReportsHelper.getFiltersInfo(setup)
# Closing the browser
setup.d.close()