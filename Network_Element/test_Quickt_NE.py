import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NFPageClass import *
from classes.Pages.NEPageClass import *
from classes.Pages.NEPageClass import *
from classes.Pages.NeNePageClass import *
from classes.Pages.QuickTrendsPageClass import *
import random
from classes.Components.SwitcherComponentClass import *
#######################################################################
# Getting Setup Details
setup = SetUp()
#######################################################################
#get time range and measures from config file
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0

measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()
#######################################################################

#######################################################################
# Logging into the appliction and launch site screen
login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

#######################################################################

#######################################################################
# get screen instance and set timerange and measure and Get the handles of the screen
# set_measure=measures[0]
# set_time=quicklinks[0]
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")
#setTimeRange(setup,set_time)
#screenInstance.measure.doSelection(siteScreenHandle,set_measure)
# sleep(5)

#Get the default selection and Validate the result
# siteScreenHandle =getHandle(setup,"site_Screen")
#sleep(5)
data1=screenInstance.btv.getData(siteScreenHandle)
print data1
length = len(data1['BTVCOLUMN1'])
rand = random.randrange(2,length)
print rand
screenInstance.btv.setSelection(rand,siteScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)

#######################################################################
#Create screen instance and get handle of screen
neScreenInstance = NEPageClass(setup.d)
neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
data2=neScreenInstance.pielegend.getData(neScreenHandle)
print data2
length = len(data2['legendText'])
print length
rand = random.randrange(0,length)
#######################################################################

neScreenInstance.pielegend.setSelection(setup.dH,[rand],neScreenHandle)
defselection = neScreenInstance.pielegend.getSelection(neScreenHandle)
print defselection

lt=defselection["legendText"][0]
print lt
index=defselection["legendText"][0].find('\n')
print index
element_name=lt[0:index]
print element_name

neScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
neScreenInstance.cm.activateContextMenuOptions(neScreenHandle)
launched = neScreenInstance.cm.launchTrends(neScreenHandle)
print launched
checkEqualAssert(launched,True, "","", "TREND IS SUCCESSFULLY LAUNCHED")

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
print xaxis
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)
print yaxis
t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)
print t

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
print list
legendname = list[0]
print legendname
checkEqualAssert(element_name,legendname,"Today","Bitrate_uplink_percentage_average","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")

