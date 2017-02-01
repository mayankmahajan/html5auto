from Utils.logger import *
from selenium import webdriver
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.QuickTrendsPageClass import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
import random
from classes.Objects.Report import *
from classes.Objects.Time import *

setup = SetUp()
# reportFilters= setup.cM.getNodeElements("reportwizardfilters","filter")
# onlyReportTypes = setup.cM.getAllNodeElements("reporttypes","reporttype")
# availableTime = setup.cM.getNodeElements("availabletimerange","time")

login(setup, "admin", "admin123")

reportTypes = setup.cM.getreportTypes()

reportObj = Report()
reportObj.filters['network']=['','','']
reportObj.filters['apnrat']=['Sushfone-1','']
reportObj.filters['subscriber']=['11']


response = createreport(setup,reportTypes[reportTypes.keys()[0]],reportObj,[Time(),Time(2017,01,14,14)])

print response[0]
print response[1]

checkEqualAssert(response[0],response[1],"","","Checking report Review Page")

setup.d.close()













