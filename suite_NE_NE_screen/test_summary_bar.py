import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
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

drilltoScreen(setup.d,setup.dH,Constants.NETWORKELEMENTS)
screenInstance = NEPageClass(setup.d)
NEScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        screenInstance.measure.doSelection(NEScreenHandle, measures[i])

        # testcase body starts
        # Get the Instance of the screen
        NEScreenHandle = getHandle(setup,Constants.NETWORKELEMENTS)
        data = screenInstance.pielegend.getData(NEScreenHandle)
        print data
        length = len(data["legendText"])
        print length
        if length == 1:
            rand=0
        else:
            rand = random.randrange(0,length)
        screenInstance.pielegend.setSelection(setup.dH,[rand],NEScreenHandle)
        defselection = screenInstance.pielegend.getSelection(NEScreenHandle)
        print defselection
        #print defselection['BTVCOLUMN2']
        lt=defselection["legendText"][0]
        print lt
        index=defselection["legendText"][0].find('\n')
        print index
        element_name=lt[0:index]
        print element_name
        element_value=lt[index+1::]
        print element_value
        values = measures[i].split('_')
        print values

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
            selections = screenInstance.summarybar.getSelection(NEScreenHandle)

            #print "hahaha"
            #print selections['All WDC']
            summarybarvalues = selections[element_name][values[0]]['Average']

        else:
            selections = screenInstance.summarybar.getSelection(NEScreenHandle)
            #print selections[btvname]
            print selections
            summarybarvalues = selections[element_name][values[0]][values[3]]






        # testcase body ends
        message = str(element_name)
        # Result Logging
        checkEqualAssert(element_value,summarybarvalues,quicklinks[t],measures[i],message)

        i+=1
        # end of measureSelection


    t+=1