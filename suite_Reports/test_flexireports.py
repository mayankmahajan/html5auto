import unittest
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

setup = SetUp()

# login(setup, "cmathieu", "a")

ar = []
reportname = "site"
login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

# suite_Reports Module
###################################
exploreScreenInstance.exploreList.launchModule(exploreHandle,"REPORTS")
# reporttype = ["Site Report Average","Network Function Report Average","Site Interaction Report Average","Site-Network Function Report Average","Site-Network Element Report Average",
#               "Site-VRF Report Average","Site Interaction-Network Function Report Average","Site Interaction-Network Element Report Average","Site Interaction-VRF Report Average"]
reports = ["Site Report","Network Function Report","Site Interaction Report","Site-Network Function Report","Site-Network Element Report","Site-VRF Report"
           ,"Site Interaction-Network Function Report","Site Interaction-Network Element Report","Site Interaction-VRF Report"]
n=[1,1,2,2,2,2,3,3,3]
avg_peak=["Average","Peak"]

for i in range(len(reports)):

    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenHandle = getHandle(setup,"report_Screen")

    reportScreenInstance.launchCreateReport(setup.d)
    grPopInstance = GenerateReportsPopClass(setup.d)
    grPopHandle = getHandle(setup,"report2_popup")
    length = len(avg_peak)
    rand = random.randrange(1,length)
    grPopInstance.reportspopup.selectRadioButton(avg_peak[rand],grPopHandle)
    grPopInstance.reportspopup.selectRadioButton(reports[i],grPopHandle)

    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.reportspopup.selectRadioButton("Today",grPopHandle)
    grPopHandle = getHandle(setup,"report2_popup")
    starttime = getInputText(grPopHandle,'generateReportDialog','starttime')
    endtime = getInputText(grPopHandle,'generateReportDialog','endtime')
    grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)

    ### Get table Data has to different for different reports####
    for j in range(0,n[i]):

        grPopHandle = getHandle(setup,"report2_popup")
        # ar.append(grPopInstance.table.selectTableCellIndex(1,grPopHandle))
        grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
        #######################    END     ###############################################
        break
    grPopHandle = getHandle(setup,"report2_popup")
    starttimeend =getInputText(grPopHandle,'generateReportDialog','starttime')
    endtimeend = getInputText(grPopHandle,'generateReportDialog','endtime')
    filters = FindWordInString(ar,grPopHandle)
    checkEqualAssert(starttime,starttimeend,"","","Start Time validation")
    checkEqualAssert(endtime,endtimeend,"","","End Time validation")
    checkEqualAssert(filters,True,"","","Filters validation")
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportnamewizard"],reportname)
    grPopInstance.dropdown.customClick(grPopHandle['generateReportDialog']["addemail"])
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInputwizard"],"deepanshu.ahuja@guavus.com")
    grPopInstance.reportspopup.clickButton("Submit",grPopHandle)
    date = currentdate()
    grPopHandle = getHandle(setup,"report2_popup")
    grPopInstance.dropdown.customClick(grPopHandle['successdialog']['ok'])

    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenHandle = getHandle(setup,"report_Screen")

    reportScreenInstance.switcher.switchTo(1,reportScreenHandle,'createdialog','switcher')
    # reportScreenHandle = getHandle(setup,"report_Screen")

    data = reportScreenInstance.table.getTableData1(getHandle(setup,"report_Screen"),"table")
    # result = data['rows'][0][1]
    # type = data['rows'][0][2]
    # reportid = IsreportIDvalid(data)
    # uidate = data['rows'][0][5]
    if (data['rows'][0][1] == reportname):
        checkEqualAssert(data['rows'][0][1],reportname,"Today","","Site Report name")
        checkEqualAssert(data['rows'][0][2],reports[i]+" "+avg_peak[rand] ,"Today","","Report Type")
        checkEqualAssert(IsreportIDvalid(data),True,"","","The Report ID")
        checkEqualAssert(data['rows'][0][5],date,"Today","","Time of the report")
    else:
        reportScreenHandle = getHandle(setup,"report_Screen")
        reportScreenInstance.switcher.switchTo(0,reportScreenHandle,'createdialog','switcher')
        reportScreenHandle = getHandle(setup,"report_Screen")
        data = reportScreenInstance.table.getTableData1(reportScreenHandle,"table")
        checkEqualAssert(data['rows'][0][1],reportname,"Today","","Site Report name")
        checkEqualAssert(data['rows'][0][2],reports[i]+" "+avg_peak[rand],"Today","","Report Type")
        checkEqualAssert(IsreportIDvalid(data),True,"","","The Report ID ")
        checkEqualAssert(data['rows'][0][4],date,"Today","","Time of the report")

# Closing the Testcase
setup.d.close()



setup.d.close()

