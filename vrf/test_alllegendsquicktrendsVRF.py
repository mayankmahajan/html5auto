from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.VrfPageClass import  *
from classes.Components.SwitcherComponentClass import *
from classes.Pages.QuickTrendsPageClass import *


# Getting Setup Details and Launching the application

######################################################
setup = SetUp()
login(setup, "admin", "Admin@123")
#####################################################


# Launch Site Screen
launchPage(setup,"site_Screen")
sleep(5)

# Get the Instance and handle of the screen
screenInstance = SitePageClass(setup.d)
siteScreenHandle = getHandle(setup,"site_Screen")


# Get the default selection

a = screenInstance.btv.setSelection(2,siteScreenHandle)
defSelection = screenInstance.btv.getSelection(siteScreenHandle)

status=drilltoScreen(setup.d,setup.dH,Constants.VRF)

vrfScreenInstance = VrfPageClass(setup.d)
vrfScreenHandle = getHandle(setup,Constants.VRF)

data = vrfScreenInstance.btv.getData(vrfScreenHandle)
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

vrfScreenInstance.cm.activateContextMenuOptions(vrfScreenHandle)

vrfScreenInstance.cm.launchTrends(vrfScreenHandle)

qtScreenInstance = QuickTrendsPageClass(setup.d)
qtScreenHandle = getHandle(setup,"qt_Screen")


xaxis  = qtScreenInstance.quicktrends.getXAxis(qtScreenHandle)
yaxis  = qtScreenInstance.quicktrends.getYAxis(qtScreenHandle)

t = qtScreenInstance.quicktrends.moveTotick(setup.dH,qtScreenHandle)

list = qtScreenInstance.quicktrends.getLegendList(qtScreenHandle)
legends = list[0]

checkEqualAssert(sitesname,legends,"","","DATA IS VALIDATE FOR ALL THE LEGENDS IN THE QUICK TRENDS")
setup.d.close()