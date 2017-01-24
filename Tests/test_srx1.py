from Utils.utility import *
from Utils.SetUp import *
from classes.Pages.TrendingMonitoringPageClass import *

setup = SetUp()
login(setup, "cmathieu", "a")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreScreenInstance.exploreList.launchScreen(getHandle(setup,"explore_Screen"),"exploreList","trendingMonitoring")
tmScreenInstance = TrendingMonitoringPageClass(setup.d)
h=getHandle(setup,"tm_Screen")
if len(h['errorhandle']['errordialog']) > 0:
    # logger.log("Error Dialog comes up")
    h['errorhandle']['errordialog'][0].find_elements_by_tag_name("button")[0].click()
handle = getHandle(setup,"tm_Screen")
tmScreenInstance.quiklinkTimeRange.setSelection1("last2Hours",getHandle(setup,"tm_Screen"),"timeRangeDiv")
tmScreenInstance.menu.setSwitcher(3,getHandle(setup,"tm_Screen"),"menu-component","togglebuttons")
tHandle = getHandle(setup,"tm_Screen")
data = tmScreenInstance.table.getTableData1(tHandle,"table")
tmScreenInstance.table.setSelection1(3,tHandle,"table")
d = tmScreenInstance.table.getDynamicText(tHandle,"table")
ccd = tmScreenInstance.collapseCharts.getSelectedData(tHandle,"collapseCharts")

# Closing the Testcase
setup.d.close()