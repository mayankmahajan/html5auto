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

setup = SetUp()

# login(setup, "cmathieu", "a")


reportname = "site"
login(setup, "admin", "Admin@123")

reports = ["Site Interaction Report","Site-Network Function Report","Site-Network Element Report","Site-VRF Report"
    ,"Site Interaction-Network Function Report","Site Interaction-Network Element Report","Site Interaction-VRF Report"]
n=[3,3,3,3,4,4,4]
for i in range(len(reports)):


    grPopInstance = GenerateReportsPopClass(setup.d)
    # grPopHandle = getHandle(setup,"report2_popup")
    # grPopInstance.reportspopup.selectRadioButton("Average",grPopHandle)
    # grPopInstance.reportspopup.selectRadioButton(reports[i],grPopHandle)

    ### Get table Data has to different for different reports####
    for el in n:
        for j in range(1,el):

            grPopHandle = getHandle(setup,"report2_popup")
            grPopInstance.table.getTableData1(grPopHandle,"table")
            grPopInstance.reportspopup.clickButton("Next Step",grPopHandle)
            #######################    END     ###############################################
        break
    grPopHandle = getHandle(setup,"report2_popup")
setup.d.close()
