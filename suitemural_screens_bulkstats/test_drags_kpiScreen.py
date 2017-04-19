from Utils.utility import *
from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from classes.Pages.TrendingMonitoringPageClass import *
from classes.Components.BaseComponentClass import *
from classes.Components.CollapsableListComponentClass import *
import MuralUtils.BulkstatsHelper as BulkstatsHelper
import MuralUtils.Helper as Helper
from classes.Components.CollapsableListComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *


setup  = SetUp()
login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
isError(setup)


exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup, "explore_Screen")
exploreScreenInstance.exploreList.switchApp(exploreHandle)
h=getHandle(setup, "explore_Screen")
list=exploreScreenInstance.exploreList.getAllApps(h)
result = exploreScreenInstance.exploreList.launchappByName(getHandle(setup, "explore_Screen"),"Bulkstats / KPIs")
time.sleep(6)
if len(setup.d.window_handles)>1:
    setup.d.switch_to.window(setup.d.window_handles[1])

exploreHandle = getHandle(setup,"explore_Screen")
exploreScreenInstance.exploreList.launchModule(exploreHandle,"KPI")

isError(setup)

globalFilterInstance = GlobalFiltersPopClass(setup.d)

cl = CollapsableListComponentClass()
Helper.clickOnfilterIcon(setup,MuralConstants.ATSCREEN)
# bulk = getHandle(setup,MuralConstants.KPISCREEN)
filters = {}
f1=cl.merge_dictionaries(filters,BulkstatsHelper.setFilter(setup,index=0,h=getHandle(setup,"bulk_popup","bulk_filter"),occurence=0))
f2=cl.merge_dictionaries(f1,BulkstatsHelper.setFilter(setup,index=0,h=getHandle(setup,"bulk_popup","bulk_filter"),occurence=1))
f3=cl.merge_dictionaries(f2,BulkstatsHelper.setFilter(setup,index=0,h=getHandle(setup,"bulk_popup","bulk_filter"),occurence=2))
cl.clickButton("Next",getHandle(setup,"bulk_popup",MuralConstants.ALLBUTTONS))
isError(setup)
f4=cl.merge_dictionaries(f3,BulkstatsHelper.setFilter(setup,index=0,h=getHandle(setup,"bulk_popup","bulk_filter"),occurence=0))
f5=cl.merge_dictionaries(f4,BulkstatsHelper.setCounters(setup,indices=[0],h=getHandle(setup,"bulk_popup","bulk_filter"),occurence=1))

cl.clickButton("Apply",getHandle(setup,"bulk_popup",MuralConstants.ALLBUTTONS))

isError(setup)


globalFilterInstance = GlobalFiltersPopClass(setup.d)
globalFilterFromScreen = Helper.getGlobalFiltersFromScreen(MuralConstants.ATSCREEN, globalFilterInstance, setup)

for key in f5.keys():
    checkEqualAssert(globalFilterFromScreen[key],globalFilterFromScreen[key],message="Global Filter verification at Screen and Filter PopUp ::key::"+key)


bulk = getHandle(setup,MuralConstants.KPISCREEN,"leftListContainer")
data = cl.getData(setup,bulk)
clIndex = cl.setIndex(setup,bulk,index=1)
isError(setup)
selections = cl.getSelectedRow(getHandle(setup,MuralConstants.KPISCREEN))

# drag_drop = BaseComponentClass()
# drag_drop = BaseComponentClass()
drags = bulk['leftListContainer']['draggables']
drops = bulk['compareContainer']['drop']
# bulk = getHandle(setup,MuralConstants.KPISCREEN)
BulkstatsHelper.checkTextAfterDrag(drags,drops[0],k=0,setup=setup)
isError(setup)
bulk = getHandle(setup,MuralConstants.KPISCREEN,"rightListContainer")
drags_2 = bulk['rightListContainer']['draggables']
BulkstatsHelper.checkTextAfterDrag(drags_2,drops[1],key1="dragg",key2="dropp",k=1,setup=setup)
isError(setup)

TMScreenInstance = TrendingMonitoringPageClass(setup.d)

tooltipData = TMScreenInstance.quicktrends.hoverOverTicksGetMainChartText(
        setup,getHandle(setup,MuralConstants.KPISCREEN,"compareContainer"),
        MuralConstants.KPISCREEN,
        parent="compareContainer",
        parent_tooltip="compareContainer"
)
isError(setup)

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
