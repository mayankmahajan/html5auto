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
if len(setup.d.window_handles)>1:
    setup.d.switch_to.window(setup.d.window_handles[1])


cl = CollapsableListComponentClass()
bulk = getHandle(setup,MuralConstants.BULKSCREEN,"leftListContainer")
data = cl.getData(setup,bulk)
isError(setup)
indx = random.randint(0,len(data))
text_to_search =  data[indx].split("\n")[0]
cl.sendkeys_input(text_to_search,bulk,0,parent="leftListContainer")
isError(setup)

bulk = getHandle(setup,MuralConstants.BULKSCREEN,parent="leftListContainer")
searcheddata = cl.getData(setup,bulk)

for el in searcheddata:
    if text_to_search in el:
        flag = True
    else:
        flag = False
        break

checkEqualAssert(True,flag,message="Checking List Container Fields after Search")
cl.clear_input(bulk,0,parent="leftListContainer")

bulk = getHandle(setup,MuralConstants.BULKSCREEN,parent="leftListContainer")
checkEqualAssert(data,cl.getData(setup,bulk),"Checking Clear Search on List Container")

setup.d.close()