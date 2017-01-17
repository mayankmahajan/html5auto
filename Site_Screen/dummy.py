# import datetime
#
# x = datetime.datetime.now()
# print x
# y =str(x).split(':')
# z = y[0]+":"+y[1]
#
# print y
# print z
# from pytz import all_timezones
#
# print len(all_timezones)
# for zone in all_timezones:
#     if 'India' in zone:
#         print zone
# import datetime
# import pytz # new import
#
# current_time = datetime.datetime.now() #system time
#
# server_timezone = pytz.timezone("US/Eastern")
# new_timezone = pytz.timezone("Canada/Central")
# print current_time
# print server_timezone
# print new_timezone
# # returns datetime in the new timezone. Profit!
# current_time_in_new_timezone = server_timezone.localize(current_time).astimezone(new_timezone)
#
# print current_time_in_new_timezone
import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.ForensicsPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")


exploreScreenInstance.exploreList.switchApp(exploreHandle,2)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])




forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")
forensicsScreenInstance.switcher.switchTo(1,forensicsScreenHandle,'createdialog','switcher')
data = forensicsScreenInstance.table.getTableData1(getHandle(setup,"forensics_Screen"),"netflowtable")

setup.d.close()