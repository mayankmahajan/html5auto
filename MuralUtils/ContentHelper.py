'''
Script will check following points:
1. Validate all the quicklnks
2. Use all the Measures + Directions
3. Set Selection from Pie Chart
4. Set Selection from Pie Legend
5. Check pie-pielegend sync
6. Validate Screen Name and Selection Label
7. Is CM enabled or disabled
8. Export to CSV
9. Goto Trends and Monitoring
10. Get BreadCrumb List (Active and Non-Active)
11. Get Tooltip from Pie Chart
'''
from Utils.SetUp import *
from MuralUtils.Helper import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *
from classes.Pages.GlobalFiltersPopClass import *

import sys


'''

    :param setup: driver and config instance
    :param intance: screen Instance
    :return: True/False

    ######
    1. Set legend -> check pie and legend selection
    2. Set pie -> check pie and legend selection
    3. UnSet legend -> check pie and legend selection
    4. UnSet pie -> check pie and legend selection
    5. Tooltip PieChart
    6. Validate data of tooltip with legend


    '''


def getSelectionsFromContent(networkScreenInstance, setup, measureSelected):


    summary={}
    summary['dim'] = []
    summary['value'] = []

    btv0 = networkScreenInstance.multibtv.getSelections(getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=0)

    btv1 = networkScreenInstance.multibtv.getSelections(getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=1)
    btv1['header'] = networkScreenInstance.multibtv.getHeader(getHandle(setup, MuralConstants.ContentScreen, "btvGroup"))

    sumSel,summary['header'] = networkScreenInstance.summarybar.getSelection2(getHandle(setup,MuralConstants.NWSCREEN,"summarybar"))
    summary['dim'] = summary['header']
    summary['value']=[sumSel[summary['dim'],0,measureSelected],
                      sumSel[summary['dim'],1,measureSelected]]

    return picker1,picker2,btv,summary






def checkSummaryBar(setup,instance,measureSelected):
    r = instance.btv.getData(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    for i in range(0, len(r['legendText'])):
        instance.btv.setSelection(i,getHandle(setup,MuralConstants.NWSCREEN,"btv"))
        isError(setup) # handles any error coming up

        selection =instance.btv.getSelection(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
        dim,value = selection['BTVCOLUMN1'],selection['BTVCOLUMN2']
        btvdata = {}
        summary = {}
        btvdata[(dim, 0, measureSelected['locatorText'])] = value
        summary['data'], summary['header'] = instance.summarybar.getSelection2(getHandle(setup,MuralConstants.NWSCREEN,"summarybar"))
        checkEqualAssert(btvdata[(dim, 0, measureSelected)], summary['data'][(dim, 0, measureSelected['locatorText'])], "", "","Verify Summary card")


def cheackHeader(setup,instance,measureSelected):

    selection=instance.btv.getSelection(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    summary = {}
    if int(len(selection['selIndices']))==0:
        summary['data'], summary['header'] = instance.summarybar.getSelection2(getHandle(setup, MuralConstants.ATSCREEN, "summarybar"))
        breadCrumbLabel = instance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
        checkEqualAssert(str(breadCrumbLabel), str(summary['header']), "", "","Verify Summary Header ")


def checkLegend(setup, instance):
    p = instance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
    for i in range(0, len(p['legendText'])):
        instance.pielegend.setSelection(setup.dH,[i],getHandle(setup, MuralConstants.ATSCREEN,"pielegend"),True)
        j = instance.piecomponent.getPieSelections(getHandle(setup, MuralConstants.ATSCREEN,"piechart"))
        k = instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
        checkEqualAssert(int(j[0]), int(k['selIndices'][0]), "", "", "Verify Selections on PieLegend and Pie for index ")

    instance.pielegend.setSelection(setup.dH, [i], getHandle(setup, MuralConstants.ATSCREEN,"pielegend"),True)
    return True



def checkAllComponent(setup,instance,quicklink,measureSelected,index,flag):
    breadCrumbLabel = instance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    if not flag:
        p1,p2,b1,s1=getSelectionsFromContent(instance, setup, measureSelected['locatorText'])

        checkEqualAssert("All",p1['dim'][0], quicklink, measureSelected['locatorText'], "Verify Default Selection at picker = "+p1['header'])
        checkEqualAssert("All",p2['dim'][0], quicklink, measureSelected['locatorText'], "Verify Default Selection at picker = "+p2['header'])
        checkEqualAssert("All",b1['dim'][0], quicklink, measureSelected['locatorText'], "Verify Default Selection at BTV = "+b1['header'])
        checkEqualAssert("All",s1['dim'], quicklink, measureSelected['locatorText'], "Verify Default Selection at summary = "+s1['header'])
        checkEqualAssert(b1['dim'][0],s1['dim'], quicklink, measureSelected['locatorText'], "Verify Default Selection at summary = "+s1['header'])
        checkEqualAssert(s1['value'][0],b1['value'][0],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, All Sub")
        checkEqualAssert(s1['value'][1],b1['value'][0],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, Per Sub")
        checkEqualAssert(s1['dim'], breadCrumbLabel, quicklink, measureSelected['locatorText'], "Verify BreadCrumb Label")
    else:
        p1,p2,b1,s1=getSelectionsFromContent(instance, setup, measureSelected['locatorText'])
        checkEqualAssert(b1['dim'][0],s1['dim'], quicklink, measureSelected['locatorText'], "Verify Selection at summary = "+s1['header'])
        checkEqualAssert(s1['dim'], breadCrumbLabel, quicklink, measureSelected['locatorText'], "Verify BreadCrumb Label")
        checkEqualAssert(s1['value'][0],b1['value'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, All Sub")
        checkEqualAssert(s1['value'][1],b1['value'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, Per Sub")

        instance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)
        instance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
        isError(setup)
        globalFilterInstance = GlobalFiltersPopClass(setup.d)
        actualFilters = getGlobalFiltersFromScreen(MuralConstants.NWSCREEN, globalFilterInstance, setup)
        for k,v in actualFilters.iteritems():
            if k in p1['header']:
                for i in range(len(p1['dim'])):
                    checkEqualAssert(p1['dim'][i],v[i],quicklink,measureSelected['locatorText'],"Verify Previous Screen Selected Dimension = "+p1['header']+"  at next Screen")
            elif k in p2['header']:
                for j in range(len(p2['dim'])):
                    checkEqualAssert(p2['dim'][j],v[j],quicklink,measureSelected['locatorText'],"Verify Previous Screen Selected Dimension = "+p2['header']+"  at next Screen")
            elif k in b1['header']:
                for l in range(len(b1['dim'])):
                    checkEqualAssert(b1['dim'][l],v[l],quicklink,measureSelected['locatorText'],"Verify Previous Screen Selected Dimension = "+b1['header']+"  at next Screen")

        # instance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup, MuralConstants.ATSCREEN, "breadcrumb"))
        instance.cm.gotoScreenViaBreadCrumb("MURAL Network Insights",getHandle(setup, MuralConstants.ATSCREEN, "breadcrumb"))
        isError(setup)

    return True

def unSetBTV(setup,instance):

    instance.btv.setSelection(0,getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    k=instance.btv.getSelection(getHandle(setup,MuralConstants.NWSCREEN,"btv"))


    # checkEqualAssert(len(i), len(j['selIndices']), "", "","Verify UnsetPie ")
    return True



def unSetpicker(index,setup, instance):
    selection = instance.picker.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.NWSCREEN,"picker"),[2,4],index,"picker")

    # checkEqualAssert(len(i), len(j['selIndices']), "", "", "Verify UnsetPie ")
    return True

def toolTip(setup,instance):
    toolTipData = instance.btv.getToolTipInfo(setup.d,setup.dH,getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    btvdata = instance.btv.getData(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    for i in range(len(toolTipData)):
        checkEqualAssert(str(toolTipData[i].split('\n')[0]),str(btvdata['BTVCOLUMN1'][i]),"","","Tootip Text Validation")
        checkEqualAssert(str(toolTipData[i].split('\n')[1]),str(btvdata['BTVCOLUMN2'][i]),"","","Tootip Value Validation")
    return True


def doActionsOnNetwork(networkScreenInstance,setup,index=2):
    # set picker 1
    picker1={}
    picker1['data'] = networkScreenInstance.picker.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.NWSCREEN,"picker"),[index,index-2],0,"picker",setup=setup)
    picker1['header'] =  networkScreenInstance.picker.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"picker"),0)



    # set picker 2
    picker2={}
    picker2['data'] = networkScreenInstance.picker.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.NWSCREEN,"picker"),[index,index-2],1,"picker",setup=setup)
    picker2['header'] =  networkScreenInstance.picker.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"picker"),1)


    # get btvdata
    btv = {}
    btv['data'] = networkScreenInstance.btv.setSelection(index,getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    btv['header'] = networkScreenInstance.btv.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"btv"),0)
    # btv['tooltip']  = networkScreenInstance.btv.getToolTipInfo(setup.d,setup.dH,getHandle(setup,MuralConstants.NWSCREEN,"btv"))

    summary = {}
    summary['data'],summary['header'] = networkScreenInstance.summarybar.getSelection2(getHandle(setup,MuralConstants.NWSCREEN,"summarybar"))

    return picker1,picker2,btv,summary


'''
try:

    setup = SetUp()
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))

    networkScreenInstance = NetworkScreenClass(setup.d)
    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    for e in quicklink:
        print qs[e]['locatorText']

    #for q in quicklink:

        accesstechnologyScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        accesstechnologyScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        accesstechnologyScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'],getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        selectedQuicklink = networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))

        screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
        breadCrumbLabel = accesstechnologyScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

        measures = setup.cM.getNodeElements("networkdimeas", "measure")
        for k, measure in measures.iteritems():
            measureSelected = accesstechnologyScreenInstance.picker.domultipleSelectionWithName(getHandle(setup, MuralConstants.ATSCREEN, "measureChangeSection"), measure['locatorText'], 0,"measureChangeSection", "measure")
            checkEqualAssert(measure['locatorText'], measureSelected, "", "", "Verify Selected measure")
            for e in range(0,3):
                if accesstechnologyScreenInstance.switcher.measureChangeSwitcher(e,getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection")):
                    selectedSwitcher = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection"))
                    checkEqualAssert([e],selectedSwitcher,"","","Verify Selected Measure Direction")
                    #checkPie(setup,accesstechnologyScreenInstance)
                    #print "checkPie Pass"
                    #checkLegend(setup,accesstechnologyScreenInstance)
                    #print "checkPieLegend Pass"
                    #unSetPie(setup,accesstechnologyScreenInstance)
                    #print "unSetPie Pass"
                    #unSetPieLegend(setup,accesstechnologyScreenInstance)
                    #print "unSetPieLegend Pass"
                    #toolTipPieAndPieLegend(setup,accesstechnologyScreenInstance)
                    #print "Validation pass for Tooltip"
                    #checkSummaryBar(setup,accesstechnologyScreenInstance,measure)
                    #cheackHeader(setup,accesstechnologyScreenInstance,measure)
                    #checkTotalSelectionOnPie(setup, accesstechnologyScreenInstance)
                    #clickOnfilterIcon()

#   breadCrumbLabel = networkScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))


    accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb("Network", getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    accesstechnologyScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    accesstechnologyScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))


except Exception as e:
    print str(e)
    # sys._current_frames()
    setup.d.close()
'''






#pie legend
# (1. get dimSelected from getSelection API,
# 2. 0/1,
# 3. measureSelected) =
# 4. get value from getSelection API




