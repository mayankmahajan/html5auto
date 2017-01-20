import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.NEPageClass import *
from classes.Pages.NeNePageClass  import *
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
NeScreenInstance = NEPageClass(setup.d)
NeScreenHandle = getHandle(setup, Constants.NETWORKELEMENTS)

NeScreenInstance.pielegend.setSelection(setup.dH,[3],NeScreenHandle)
drilltoScreen(setup.d,setup.dH,Constants.NENE)

NeneScreenInstance=NeNePageClass(setup.d)

# Get the handles of the nene screen
NeneScreenHandle = getHandle(setup,Constants.NENE)

while t < timeIteration:
    i=0
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        NeneScreenInstance.measure.doSelection(NeneScreenHandle, measures[i])

        # testcase body starts
        # Get the Instance of the screen
        NeneScreenHandle = getHandle(setup, Constants.NENE)
        data = NeneScreenInstance.btv.getData(NeneScreenHandle)
        print data
        length = len(data['BTVCOLUMN1'])
        print length
        rand = random.randrange(1,length)
        NeneScreenInstance.btv.setSelection(rand,NeneScreenHandle)
        NeneScreenHandle = getHandle(setup,Constants.NENE)
        defselection = NeneScreenInstance.btv.getSelection(NeneScreenHandle)
        print defselection
        btvvalue = defselection['BTVCOLUMN2']
        print btvvalue
        btvname = defselection['BTVCOLUMN1']
        print btvname

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
            selections = NeneScreenInstance.summarybar.getSelection(NeneScreenHandle)
            print selections
            summarybarvalues = selections[btvname][values[0]]['Average']

        else:
            selections = NeneScreenInstance.summarybar.getSelection(NeneScreenHandle)
            print selections
            summarybarvalues = selections[btvname][values[0]][values[3]]
            print summarybarvalues

        # testcase body ends
        message = str(btvname)
        # Result Logging
        checkEqualAssert(btvvalue,summarybarvalues,quicklinks[t],measures[i],message)

        i+=1
        # end of measureSelection
    t+=1
