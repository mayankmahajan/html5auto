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
siteIteration = len(setup.cM.getNodeElements("sitetypes","sitetype"))
sites = setup.cM.getNodeElements("sitetypes","sitetype").keys()

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



#selections = screenInstance.summarybar.getSelection(siteScreenHandle)


# while loop is to iterate over all the quicklinks
while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < siteIteration:
        j=0
        screenInstance.measure.doSelectionSite(siteScreenHandle,sites[i])

        # testcase body starts

        # while loop is to iterate over all the measure
        while j < measureIteration:
            screenInstance.measure.doSelection(siteScreenHandle,measures[j])

            # testcase body starts
            # Get the Instance of the screen
            screenInstance = SitePageClass(setup.d)

            # Get the handles of the screen
            siteScreenHandle = getHandle(setup,"site_Screen")
            data = screenInstance.btv.getData(siteScreenHandle)
            length = len(data['BTVCOLUMN1'])
            rand = random.randrange(1,length)
            screenInstance.btv.setSelection(rand,siteScreenHandle)
            defselection = screenInstance.btv.getSelection(siteScreenHandle)
            #print defselection['BTVCOLUMN2']
            btvvalue = defselection['BTVCOLUMN2']
            btvname = defselection['BTVCOLUMN1']

            values = measures[j].split('_')

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
                selections = screenInstance.summarybar.getSelection(siteScreenHandle)
                #print "hahaha"
                #print selections['All WDC']
                summarybarvalues = selections[btvname][values[0]]['Average']

            else:
                selections = screenInstance.summarybar.getSelection(siteScreenHandle)
                #print selections[btvname]
                summarybarvalues = selections[btvname][values[0]][values[3]]






            # testcase body ends
            message = "Data validated with summary bar " + str(btvname) + " " + sites[i]
            # Result Logging
            checkEqualAssert(btvvalue,summarybarvalues,quicklinks[t],measures[i],message)
            j+=1
        # end of measureSelection






        # testcase body ends

        # Result Logging
        expected = "True"
        actual = "True"


        # checkEqualAssert(expected,actual,quicklinks[t],sites[i])

        i+=1
        # end of measureSelection


    t+=1
    # end of while loop for QuicklinkSelections


# Closing the Testcase
setup.d.close()



