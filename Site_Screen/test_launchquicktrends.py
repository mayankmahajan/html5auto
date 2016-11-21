from Utils.utility import *
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.SitePageClass import *
from classes.Components.SearchComponentClass import *
from classes.Pages.QuickTrendsPageClass import *



# Getting Setup Details
setup = SetUp()


# Launching Application
login(setup, "admin", "Admin@123")


# Launch Screen
launchPage(setup,Constants.SITES)

# Get the Instance of the screen
screenInstance = SitePageClass(setup.d)

# Get the handles of the screen
siteScreenHandle = getHandle(setup,"site_Screen")

# Set the bar Table view to the 2 index
screenInstance.btv.setSelection(3,siteScreenHandle)

selection = screenInstance.btv.getSelection(siteScreenHandle)

screenInstance.cm.activateContextMenuOptions(siteScreenHandle)

screenInstance.cm.launchTrends(siteScreenHandle)


setup.d.close()

