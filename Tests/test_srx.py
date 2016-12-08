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
from classes.Pages.EventDriversPageClass import *

setup = SetUp()
login(setup, "cmathieu", "a")
exploreScreenInstance = ExplorePageClass(setup.d)
# exploreScreenHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(getHandle(setup,"explore_Screen"),"exploreList","eventdriver1")

edScreenInstance = EventDriversPageClass(setup.d)

edScreenInstance.pielegend.setSelection1(setup.dH,[3],getHandle(setup,"ed_Screen"),'pielegend1')
edScreenInstance.pielegend.setSelection1(setup.dH,[1],getHandle(setup,"ed_Screen"),'pielegend2')


p1 = edScreenInstance.pielegend.getData1(getHandle(setup,"ed_Screen"),'pielegend1')
p2 = edScreenInstance.pielegend.getData1(getHandle(setup,"ed_Screen"),'pielegend2')

t1 = edScreenInstance.pie.getToolTipInfo1(setup.d,setup.dH,getHandle(setup,"ed_Screen"),'piechart1')
t2 = edScreenInstance.pie.getToolTipInfo1(setup.d,setup.dH,getHandle(setup,"ed_Screen"),'piechart2')

########################################################################


# Closing the Testcase
setup.d.close()