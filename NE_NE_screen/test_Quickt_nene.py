import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NeNePageClass import *
from classes.Pages.QuickTrendsPageClass import *
import random
from classes.Components.SwitcherComponentClass import *


#######################################################################
# Getting Setup Details
setup = SetUp()
#######################################################################


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
launchPage(setup,"site_Screen")
sleep(5)
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
sleep(5)
data1=screenInstance.btv.getData(siteScreenHandle)
print data1
length = len(data1['BTVCOLUMN1'])
rand = random.randrange(2,length)
screenInstance.btv.setSelection(rand,siteScreenHandle)
#screenInstance.btv.setSelection(2,siteScreenHandle)
status=drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)

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

#select any pielagent on ne screen and verify selection
neScreenInstance.pielegend.setSelection(setup.dH,[rand],neScreenHandle)
#Drill to nene screen and verify

drilltoScreen(setup.d,setup.dH,Constants.NENE)
neneScreenInstance=NeNePageClass(setup.d)
neneScreenHandle = getHandle(setup,Constants.NENE)
data3=neneScreenInstance.btv.getData(neneScreenHandle)
print data3

length = len(data3['BTVCOLUMN1'])
rand = random.randrange(2,length)
neneScreenInstance.btv.setSelection(rand,neneScreenHandle)
# Set the bar Table view to the 2 index
#neneScreenInstance.btv.setSelection(2,neneScreenHandle)
selection = neneScreenInstance.btv.getSelection(neneScreenHandle)
singlesitename = selection['BTVCOLUMN1']
print singlesitename

neneScreenHandle = getHandle(setup, Constants.NENE)
neneScreenInstance.cm.activateContextMenuOptions(neneScreenHandle)
launched = neneScreenInstance.cm.launchTrends(neneScreenHandle)
print launched
checkEqualAssert(launched, True, "","", "TREND IS SUCCESSFULLY LAUNCHED")

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)
t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
print list
legendname = list[0]
legendname1=list[1]
print legendname
print legendname1

checkEqualAssert(singlesitename,legendname,"","","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")



# qtScreenInstance = QuickTrendsPageClass(setup.d)
# qtScreenHandle = getHandle(setup, "qt_Screen")

# sitesname = ""
# for index in range(2,len(data['BTVCOLUMN1'])):
#     print data['BTVCOLUMN1'][index]
#     sitesname = sitesname + data['BTVCOLUMN1'][index]
# print sitesname


# while t < timeIteration:
#     i=0
#     setTimeRange(setup,quicklinks[t])
#
#     # while loop is to iterate over all the measure
#     while i < measureIteration:
#         print measures[i]
#         neneScreenInstance.measure.doSelection(neneScreenHandle, measures[i])
#         qtScreenInstance = QuickTrendsPageClass(setup.d)
#         qtScreenHandle = getHandle(setup, "qt_Screen")
#
#         xaxis = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
#         print xaxis
#         yaxis = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)
#         t = qtScreenInstance.quicktrends.moveTotick(setup.dH, qtScreenHandle)
#         print t
#
#         list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
#         print list
#         legendname = list
#         print legendname
#
#         checkEqualAssert(singlesitename, legendname,quicklinks[t],measures[i],"DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")
# # neneScreenHandle = getHandle(setup,Constants.NENE)
# neneScreenInstance.cm.activateContextMenuOptions(neneScreenHandle)
#
#
# launched=neneScreenInstance.cm.launchTrends(neneScreenHandle)
# print launched
# checkEqualAssert(launched,True,set_time,set_measure,"TREND IS SUCCESSFULLY LAUNCHED")
#
# qtScreenInstance = QuickTrendsPageClass(setup.d)
# qtScreenHandle = getHandle(setup,"qt_Screen")
#
# xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
# print xaxis
# yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)
# t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)
# print t
#
# list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
# print list
# legendname = list
# print legendname
#
# checkEqualAssert(singlesitename,legendname,"","","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")
#
