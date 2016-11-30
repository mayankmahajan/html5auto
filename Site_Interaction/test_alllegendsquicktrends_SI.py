from Utils.utility import *
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.QuickTrendsPageClass import *
from classes.Pages.SiteIntScreenClass import *


# Getting Setup Details and Launching the application
setup = SetUp()

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

# Checking drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

# Get the Instance of the screen
sitescreenInstance = SiteIntScreenClass(setup.d)

# Get the handles of the screen
siteintScreenHandle = getHandle(setup,"siteInteraction_Screen")

data = sitescreenInstance.btv.getData(siteintScreenHandle)
#btvdata = getBTVData(setup.d,setup.dH)
#print data
# print data['BTVCOLUMN1']
# print data['BTVCOLUMN1'][1]
# print data['BTVCOLUMN1'][2]
# print data['BTVCOLUMN1'][3]
# length = len(data['BTVCOLUMN1'])
# index = 2
sitesname = ""
for index in range(2,len(data['BTVCOLUMN1'])):
    print data['BTVCOLUMN1'][index]
    sitesname = sitesname + data['BTVCOLUMN1'][index]

print sitesname
# print a

sitescreenInstance.cm.activateContextMenuOptions(siteintScreenHandle)

sitescreenInstance.cm.launchTrends(siteintScreenHandle)

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")


xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)

t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
legends = list[0]

checkEqualAssert(sitesname,legends,"","","DATA IS VALIDATE FOR ALL THE LEGENDS IN THE QUICK TRENDS")
setup.d.close()