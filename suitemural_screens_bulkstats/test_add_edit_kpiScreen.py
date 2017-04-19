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

globalFilterInstance = GlobalFiltersPopClass(setup.d)


for iteration in setup.cM.getNodeElements("kpiformulae","formula"):

    globalFilterInstance.clickLink("Add KPI",getHandle(setup,MuralConstants.KPISCREEN,MuralConstants.ALLLINKS))
    input=BulkstatsHelper.setFilter(setup,index=2,h=getHandle(setup,"kpi_popup","bulk_filter"),occurence=0)
    # input={}
    input['formula']=BulkstatsHelper.setFormula(setup,getHandle(setup,MuralConstants.KPIPOPUP),formulaId=iteration)
    commonelement = BaseComponentClass()

    input['rulename']=str(commonelement.sendkeys_input("RuleName"+str(random.randint(111,9999)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0))
    input['desc']=str(commonelement.sendkeys_input("Description"+str(random.randint(111,9999)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1))
    input['lthreshold']=str(commonelement.sendkeys_input(str(random.randint(0,50)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0,child="number"))
    input['uthreshold']=str(commonelement.sendkeys_input(str(random.randint(50,100)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1,child="number"))
    commonelement.clickButton("Add",getHandle(setup,"kpi_popup",MuralConstants.ALLBUTTONS))


    cl = CollapsableListComponentClass()
    bulk = getHandle(setup,MuralConstants.KPISCREEN,parent="leftListContainer")

    commonelement.sendkeys_input(input['rulename'],bulk,0,parent="leftListContainer")
    bulk = getHandle(setup,MuralConstants.KPISCREEN,parent="leftListContainer")
    clIndex = cl.setIndex(setup,bulk,index=0)
    selectedRowHandle = cl.getSelectedRowHandle(bulk)
    parents,childs = cl.getParentChilds(bulk)
    total = BulkstatsHelper.calculateValue([selectedRowHandle],childs)

    bulk_right = getHandle(setup,MuralConstants.KPISCREEN,"rightListContainer")

    data = cl.getData(setup,bulk_right,parent="rightListContainer")
    t=0
    for el in data:
        t=t+int(el.split("\n")[1])
    checkEqualAssert(t,total,message="Verifying Total from Indices")
    checkEqualAssert(True, input['rulename'] in data, message="Checking KPI Rule created")
    checkEqualAssert(input['formula'],str(selectedRowHandle.text.split("\n")[1]),message="Checking created KPI Rule for Formula")
    BulkstatsHelper.checkSeverity(setup,input,selectedRowHandle)

    # editing
    getHandle(setup,MuralConstants.KPISCREEN,"leftListContainer")["leftListContainer"]["edit"][0].click()
    checkEqualAssert(input['rulename'],
                     commonelement.getValue_input(getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0),
                     message="Verifying RuleName on Edit KPI Screen"
                     )

    checkEqualAssert(input['desc'],
                     commonelement.getValue_input(getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1),
                     message="Verifying RuleName on Edit KPI Screen"
                     )

    checkEqualAssert(input['lthreshold'],
                     commonelement.getValue_input(getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0,child="number"),
                     message="Verifying RuleName on Edit KPI Screen"
                     )

    checkEqualAssert(input['uthreshold'],
                     commonelement.getValue_input(getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1,child="number"),
                     message="Verifying RuleName on Edit KPI Screen"
                     )

    input['desc']=str(commonelement.sendkeys_input("Description"+str(random.randint(111,9999)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1))
    input['lthreshold']=str(commonelement.sendkeys_input(str(random.randint(0,50)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0,child="number"))
    input['uthreshold']=str(commonelement.sendkeys_input(str(random.randint(50,100)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),1,child="number"))
    input['rulename']=str(commonelement.sendkeys_input("RuleName"+str(random.randint(111,9999)),getHandle(setup,"kpi_popup",MuralConstants.ALLINPUTS),0))
    input['formula']=BulkstatsHelper.setFormula(setup,getHandle(setup,MuralConstants.KPIPOPUP),formulaId=iteration,force_clear=True)

    commonelement.clickButton("Update",getHandle(setup,"kpi_popup",MuralConstants.ALLBUTTONS))

    cl = CollapsableListComponentClass()
    bulk = getHandle(setup,MuralConstants.KPISCREEN,parent="leftListContainer")

    commonelement.sendkeys_input(input['rulename'],bulk,0,parent="leftListContainer")
    bulk = getHandle(setup,MuralConstants.KPISCREEN,parent="leftListContainer")
    clIndex = cl.setIndex(setup,bulk,index=0)
    selectedRowHandle = cl.getSelectedRowHandle(bulk)
    parents,childs = cl.getParentChilds(bulk)
    total = BulkstatsHelper.calculateValue([selectedRowHandle],childs)

    bulk_right = getHandle(setup,MuralConstants.KPISCREEN,"rightListContainer")

    data = cl.getData(setup,bulk_right,parent="rightListContainer")
    t=0
    for el in data:
        t=t+int(el.split("\n")[1])
    checkEqualAssert(t,total,message="Verifying Total from Indices")
    checkEqualAssert(True, input['rulename'] in data, message="Checking KPI Rule created")
    checkEqualAssert(input['formula'],str(selectedRowHandle.text.split("\n")[1]),message="Checking created KPI Rule for Formula")
    BulkstatsHelper.checkSeverity(setup,input,selectedRowHandle)







