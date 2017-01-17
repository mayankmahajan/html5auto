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


login(setup, "admin", "Admin@123")


b = []
grPopInstance = GenerateReportsPopClass(setup.d)
grPopHandle = getHandle(setup,"report2_popup")

# grPopInstance.table.getTableData1(grPopHandle)
a  = grPopInstance.table.getTableCells(grPopHandle)
print a
grPopInstance.table.selectTableCellIndex(1,grPopHandle)

setup.d.close()