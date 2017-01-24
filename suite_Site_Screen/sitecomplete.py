import unittest
from Utils.logger import *
from selenium import webdriver
import random

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *



######################## COMPLETE SITE SCREEN #########################

# Getting Setup Details and launching the application
setup = SetUp()

timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0


# Getting Measures Info from Config Files
siteIteration = len(setup.cM.getNodeElements("sitetypes","sitetype"))
sites = setup.cM.getNodeElements("sitetypes","sitetype").keys()

# Getting Measures Info from Config Files
measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()

# Logging into the setup
result = login(setup, "admin", "Admin@123")
############################# LOGIN ###################################
#Checking the login functionality
checkEqualAssert("True",str(result),"TODAY","","LOGIN SUCCESSFULL")
############################# LOGIN COMPLETED #########################

############################# SITE LAUCNHES #########################

exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")

sitescreen =exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")
# Checking the launch page of the site page
checkEqualAssert(sitescreen,True,"","","SITE PAGE LAUNCHES SUCCESSFULLY")

###########################SITE LAUNCHES COMPLETED####################
# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

######################################### DEFAULT SELECTION ######################
# Get the default selection
defSelection = screenInstance.btv.getSelection(siteScreenHandle)


# Validating the result
checkEqualAssert(str(1),str(defSelection['selIndex']),"","","DEFAULT SELECTION IS CORRECT")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(3,siteScreenHandle)


########################## DEFAULT SELECTION COMPLETED #################################

########################## SEARCH FUNCTIONALITY ##################################

alphabets = screenInstance.searchComp.setSearchText(siteScreenHandle,"branch")
time.sleep(2)

#text = screenInstance.searchComp.getSearchText(siteScreenHandle)

if(alphabets==True):
    screenInstance.searchComp.hitSearchIcon(siteScreenHandle)
    time.sleep(10)
    checkEqualAssert(True,alphabets,"","","Search_passed_for_branch")
else:
    checkEqualAssert(False,alphabets,"","","Search_failed_for_branch")

screenInstance.searchComp.hitSearchIcon(siteScreenHandle)

######################## SEARCH COMPLETED ####################################

######################## SUMMARY CARD ############################

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
measures = "Bitrate_total_absolute_peak"
i=0
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
setup.d.close()

