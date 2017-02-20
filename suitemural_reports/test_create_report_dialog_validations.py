import os

from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Objects.Time import *
from classes.Pages.ReportsModuleClass import *
from Utils.utility import *

# Launches the application
setup = SetUp()
sleep(15)

# Logins to app with credentials provided
login(setup, "admin", "admin123")

print isError(setup)

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")

print isError(setup)

# Getting reporttypes from xmls
reportTypes = setup.cM.getAllreportTypes()  # gets all reporttype combinations (56 for mural)
# reportTypes = setup.cM.getUserReportTypes() # gets only userspecific reporttypes


# Create Report Object that contains reportName,email,filters
reportObj = Report()
reportObj.filters['network']=[[1],'','']
reportObj.filters['apnrat']=[[1,2],'']  #sample of selection of filters based on index
# reportObj.filters['apnrat']=['Sushfone-1',''] #sample of selection of filters based on name
reportObj.filters['subscriber']=['11']

# creates all reporttypes and log results
ReportsHelper.checkReportsReviewPage(setup, reportTypes[0], reportObj, [Time(2015, 11, 30, 19), Time(2015, 11, 30, 21)])

# Closing the browser
setup.d.close()