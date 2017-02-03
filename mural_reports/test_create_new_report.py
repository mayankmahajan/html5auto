from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
import os
from classes.Objects.Report import *
from classes.Objects.Time import *
from Utils import ReportsHelper

setup = SetUp()

login(setup, "admin", "admin123")

reportTypes = setup.cM.getAllreportTypes()
# reportTypes = setup.cM.getUserReportTypes()

reportObj = Report()
reportObj.filters['network']=['','','']
reportObj.filters['apnrat']=[[1,2],'']
# reportObj.filters['apnrat']=['Sushfone-1','']
reportObj.filters['subscriber']=['11']

print os.path.relpath(__file__)

for reportType in reportTypes:
    logger.debug("Creating Report %s",reportType)
    print reportType
    response = ReportsHelper.createreport(setup,reportType,reportObj,[Time(),Time(2017,01,14,14)])
    ReportsHelper.checkReportTableForCreatedRecord(setup,response[0])

# Closing the browser
setup.d.close()