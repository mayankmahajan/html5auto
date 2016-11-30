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

# Launch Site Screen
launchPage(setup,"site_Screen")
sleep(5)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(3,siteScreenHandle)

selection = screenInstance.btv.getSelection(siteScreenHandle)
singlesitename = selection['BTVCOLUMN1']

siteScreenHandle = getHandle(setup,"site_Screen")


screenInstance.cm.activateContextMenuOptions(siteScreenHandle)

screenInstance.cm.launchTrends(siteScreenHandle)

checkEqualAssert(True,True,"TODAY","","TREND IS SUCCESSFULLY LAUNCHED")


qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
legendname = list[0]

checkEqualAssert(singlesitename,legendname,"TODAY","","DATA IS VALIDATE FOR THE SINGLE LEGEND IN THE QUICK TRENDS")


############ MULTIPLE SELECTION IS NOT ADDED TILL NOW #################


setup.d.close()





