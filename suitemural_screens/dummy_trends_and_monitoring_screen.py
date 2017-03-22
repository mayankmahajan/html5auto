from MuralUtils import NetworkHelper
from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Pages.QuickTrendsPageClass import *
from MuralUtils.MuralConstants import *
from classes.Components.WorkflowStartComponent import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *
from Utils.utility import *

# try:
setup =SetUp()
# Launching Network Screen
sleep(8)
login(setup,"admin","Admin@123")
wfstart = WorkflowStartComponentClass()
sleep(8)
wfstart.launchScreen("Trend",getHandle(setup,MuralConstants.WFSTARTSCREEN))

globalFilterInstance = GlobalFiltersPopClass(setup.d)


tmScreenInstance = TrendingMonitoringPageClass(setup.d)

qtScreenHandle = getHandle(setup,MuralConstants.TMSCREEN)
tmScreenInstance.quicktrends.getChartsCount(getHandle(setup,MuralConstants.TMSCREEN))

tmScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(
        getHandle(setup,MuralConstants.TMSCREEN,"trend-main"),
    1,
    index=1,
    parent="trend-main"
)
data = tmScreenInstance.quicktrends.hoverOverTicks(setup,getHandle(setup,MuralConstants.TMSCREEN),MuralConstants.TMSCREEN)
l1  = tmScreenInstance.quicktrends.getLegends_tm(getHandle(setup,MuralConstants.TMSCREEN))
p1 = tmScreenInstance.quicktrends.getPaths(getHandle(setup,MuralConstants.TMSCREEN))
c1 = tmScreenInstance.quicktrends.clickLegendByIndex_tm(2,getHandle(setup,MuralConstants.TMSCREEN,"trend-legend"))
checkEqualAssert(True,c1 in p1,message="Checking disabled color in previous view. Color = " + c1 )

p2 = tmScreenInstance.quicktrends.getPaths(getHandle(setup,MuralConstants.TMSCREEN))
checkEqualAssert(False,p1==p2,message="Line Chart should not show deactivated Dimension")
checkEqualAssert(True,c1 in p1,message="Line Chart should not show deactivated Dimension Color = " + c1)
checkEqualAssert(False,p1==p2,message="Line Chart should not show deactivated Dimension")

compareTrend1 = tmScreenInstance.quicktrends.getPaths(getHandle(setup,MuralConstants.TMSCREEN),parent="trend-compare",indexOfComp=0)
print data





setup.d.close()
# except Exception as e:
#     print str(e)
#     sys._current_frames()
    # setup.d.close()
    # raise e



