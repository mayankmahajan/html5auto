import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *

# Getting Setup Details and Launching the application
setup = SetUp()

# Getting TimeRange Info from Config Files
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()


# Logging into the appliction
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,"site_Screen")


# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        setMeasure(setup,measures[i],Constants.SITEINTERACTIONS)

        # testcase body starts
        # Get the Instance of the screen
        screenInstance = SitePageClass(setup.d)

        # Get the handles of the screen
        siteScreenHandle = getHandle(setup,Constants.SITEINTERACTIONS)
        rand = random.randrange(1,4)
        screenInstance.btv.setSelection(rand,siteScreenHandle)
        defselection = screenInstance.btv.getSelection(siteScreenHandle)
        #print defselection['BTVCOLUMN2']
        btvvalue = defselection['BTVCOLUMN2']

        values = measures[i].split('_')

        try:
            if (values[3]=="average"):
                values[3]="Average"
        except:
            print "Average is not there"

        try:
            if (values[3]=="peak"):
                values[3]=="Peak"
        except:
            print "PEak is not there"

        if (values[0]=="Wan-Cost($)"):
            values[0] = "Wan Cost($)"
            selections = screenInstance.summarybar.getSelection(siteScreenHandle)
            #print selections['All WDC']
            summarybarvalues = selections['All WDC'][values[0]]['Average']

        else:
            selections = screenInstance.summarybar.getSelection(siteScreenHandle)
            #print selections['All WDC']
            summarybarvalues = selections['All WDC'][values[0]][values[3]]






        # testcase body ends

        # Result Logging
        checkEqualAssert(btvvalue,summarybarvalues,quicklinks[t],measures[i],"Data validated with summary bar")

        i+=1
        # end of measureSelection


    t+=1
    # end of while loop for QuicklinkSelections
#
#
# a = "Wan-Cost($)_total_percentage"
# setMeasure(setup,"Wan-Cost($)_total_percentage","site_Screen")
# b = a.split('_')
# print b
# print b[0]
# print b[1]
# print b [2]
# selections = screenInstance.summarybar.getSelection(siteScreenHandle)
# print selections['All WDC']

# Logging out of the application
setup.d.close()


