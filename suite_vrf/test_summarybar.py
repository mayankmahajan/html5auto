import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.VrfPageClass import *
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

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the Index value at 2
screenInstance.btv.setSelection(2,siteScreenHandle)

# Drill to the Site Interaction Screen

drilltoScreen(setup.d,setup.dH,Constants.VRF)
screenInstance = VrfPageClass(setup.d)
VRFScreenHandle = getHandle(setup, Constants.VRF)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        print i
        screenInstance.measure.doSelection(VRFScreenHandle, measures[i])

        # testcase body starts
        # Get the Instance of the screen
        VRFScreenHandle = getHandle(setup, Constants.VRF)
        data = screenInstance.btv.getData(VRFScreenHandle)
        print data
        length = len(data['BTVCOLUMN1'])
        print length
        rand = random.randrange(1,length)
        print rand
        screenInstance.btv.setSelection(rand,VRFScreenHandle)
        time.sleep(20)
        defselection = screenInstance.btv.getSelection(VRFScreenHandle)
        print defselection
        #print defselection['BTVCOLUMN2']

        btvvalue = defselection['BTVCOLUMN2']
        btvname = defselection['BTVCOLUMN1']

        values = measures[i].split('_')

        try:
            if (values[3]=="average"):
                values[3]="Average"
        except:
            print "Average is not there"

        try:
            if (values[3]=="peak"):
                values[3]="Peak"

        except:
            print "Peak is not there"

        if (values[0]=="Wan-Cost($)"):
            values[0] = "Wan Cost($)"
            selections = screenInstance.summarybar.getSelection(VRFScreenHandle)
            print selections
            #print "hahaha"
            #print selections['All WDC']
            summarybarvalues = selections[btvname][values[0]]['Average']

        else:
            selections = screenInstance.summarybar.getSelection(VRFScreenHandle)
            #print selections[btvname]
            print selections
            summarybarvalues = selections[btvname][values[0]][values[3]]






        # testcase body ends
        message = str(btvname)
        # Result Logging
        checkEqualAssert(btvvalue,summarybarvalues,quicklinks[t],measures[i],message)

        i+=1
        # end of measureSelection


    t+=1

setup.d.close()