import os

from MuralUtils import ReportsHelper
from Utils.SetUp import *
from classes.Objects.Time import *
from classes.Pages.ReportsModuleClass import *
from Utils.utility import *

try:
    # Launches the application
    setup = SetUp()


    # Logins to app with credentials provided
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)

    # grPopInstance = GenerateReportsPopClass(setup.d)
    # ReportsHelper.checkErrorMessageAndType(setup,grPopInstance)

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
    ReportsHelper.createreport(setup, reportTypes, reportObj, [Time(), Time(2017, 01, 14, 14)])

    # Closing the browser
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
    raise e

