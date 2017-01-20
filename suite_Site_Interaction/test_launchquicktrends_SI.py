from Utils.utility import *
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.QuickTrendsPageClass import *


# Getting Setup Details and Launching the application
setup = SetUp()

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

# Checking drill to the Site Interaction Screen
drilltoScreen(setup.d,setup.dH,Constants.SITEINTERACTIONS)

# Get the Instance of the screen
sitescreenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteintScreenHandle = getHandle(setup,"site_Screen")

# Set the bar Table view to the 2 index
sitescreenInstance.btv.setSelection(2,siteintScreenHandle)

selection = sitescreenInstance.btv.getSelection(siteintScreenHandle)
singlesitename = selection['BTVCOLUMN1']

siteScreenHandle = getHandle(setup,Constants.SITEINTERACTIONS)


sitescreenInstance.cm.activateContextMenuOptions(siteScreenHandle)

sitescreenInstance.cm.launchTrends(siteScreenHandle)

checkEqualAssert(True,True,"TODAY","","TREND IS SUCCESSFULLY LAUNCHED")


qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
legendname = list[0]

checkEqualAssert(singlesitename,legendname,"TODAY","","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")

xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)



t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)

############ MULTIPLE SELECTION IS NOT ADDED TILL NOW #################
