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
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *

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

def checkPie(setup, instance):
    p = getHandle(setup, MuralConstants.ATSCREEN,"piechart")
    r = instance.pielegend.getData11(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))

    for i in range(0,len(p['piechart']['arcs'])):
        instance.piecomponent.setSelection(i,getHandle(setup, MuralConstants.ATSCREEN),True)
        j=instance.piecomponent.getPieSelections(getHandle(setup, MuralConstants.ATSCREEN))
        k=instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN))
        checkEqualAssert(int(j[0]),int(k['selIndices'][0]),"","","Verify Selections on Pie and Pie Legend")

        dim, value = instance.piecomponent.getPieSelectionText(p, "piechart", "selectionText")
        checkEqualAssert(True, dim.strip("...") in str(r['legendText'][i].split('\n')[0]), "", "","Tootip Text Validation")
        checkEqualAssert(value,str(r['legendText'][i].split('\n')[1]), "", "","Tootip Value Validation")

    instance.piecomponent.setSelection(i,getHandle(setup, MuralConstants.ATSCREEN),True)


    return True

def checkTotalSelectionOnPie(setup, instance):
    p = getHandle(setup, MuralConstants.ATSCREEN, "piechart")
    instance.pielegend.setSelection(setup.dH, [2], getHandle(setup, MuralConstants.ATSCREEN,"pielegend"), True)
    instance.piecomponent.setTotalSelectionOnPie(p, "piechart", "selectionText")
    j = instance.piecomponent.getPieSelections(p)
    k = instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
    checkEqualAssert(len(j), len(k['selIndices']), "", "", "Verify Selections on PieLegend and Pie for index ")


def checkSummaryBar(setup,instance,measureSelected):
    p = instance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))
    for i in range(0, len(p['legendText'])):
        instance.pielegend.setSelection(setup.dH, [i], getHandle(setup, MuralConstants.ATSCREEN,"pielegend"), True)
        r = instance.pielegend.getData11(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
        #dim, value = instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN))
        dim,value = str(r['legendText'][i].split('\n')[0]),str(r['legendText'][i].split('\n')[1])
        piedata = {}
        summary = {}
        piedata[(dim, 0, measureSelected['locatorText'])] = value
        summary['data'], summary['header'] = instance.summarybar.getSelection2(getHandle(setup,MuralConstants.ATSCREEN,"summarybar"))
        checkEqualAssert(piedata[(dim, 0, measureSelected)], summary['data'][(dim, 0, measureSelected['locatorText'])], "", "","Verify Summary card")


def cheackHeader(setup,instance,measureSelected):
    k=instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
    summary = {}
    if int(len(k['selIndices']))==0:
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



def checkAllComponentRelatedToPie(setup,instance,quicklink,measureSelected,index,flag):
    summary = {}
    pie = getHandle(setup, MuralConstants.ATSCREEN, "piechart")
    pielegend= getHandle(setup, MuralConstants.ATSCREEN,"pielegend")

    breadCrumbLabel = instance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    summary['data'], summary['header'] = instance.summarybar.getSelection2(getHandle(setup, MuralConstants.ATSCREEN, "summarybar"))
    dim_tooltip, value_tooltip = instance.piecomponent.getPieSelectionText(pie, "piechart", "selectionText")

    if not flag:
        j = instance.piecomponent.getPieSelections(pie)
        k = instance.pielegend.getSelection(pielegend)
        checkEqualAssert(len(j), len(k['selIndices']), quicklink, measureSelected['locatorText'], "Verify PieLegend with PieChart ")

        pieheader = instance.pielegend.getHeader(pielegend)
        # for offline demo
        # pieheader=pieheader+":"+"220.3"
        dim, value = str(pieheader.split(":")[0]),str(pieheader.split(":")[1]).strip()

        checkEqualAssert(True, dim_tooltip.strip("...") in dim, quicklink, measureSelected['locatorText'],"Tootip Text Validation with PieLegend Header")
        checkEqualAssert(dim, breadCrumbLabel, quicklink, measureSelected['locatorText'], "Verify Label")
        checkEqualAssert(dim, str(summary['header']), quicklink, measureSelected['locatorText'], "Verify Summary Header with breadCrumbLabel ")

        checkEqualAssert(str(value_tooltip), value, quicklink, measureSelected['locatorText'], "Tootip Value Validation with PieLegend")
        #checkEqualAssert(value, str(summary['data'][(dim, 0, measureSelected['locatorText'])]),"", "", "Verify Summary Data Value for All Sub")

        # Need clarifications on How to calculate PerSub Value
        #checkEqualAssert(value, str(summary['data'][(dim, 1, measureSelected['locatorText'])]), "", "","Verify Summary Data Value for per Sub")

    else:
        j = instance.piecomponent.getPieSelections(pie)
        k = instance.pielegend.getSelection(pielegend)
        r = instance.pielegend.getData11(pielegend)
        checkEqualAssert(int(j[0]), int(k['selIndices'][0]), quicklink, measureSelected['locatorText'],"Verify Selections on PieLegend and Pie for index ")
        dim, value = str(r['legendText'][index].split('\n')[0]), str(r['legendText'][index].split('\n')[1])


        checkEqualAssert(True, dim_tooltip.strip("...") in dim, quicklink, measureSelected['locatorText'],"Tootip Text Validation with PieLegend")
        checkEqualAssert(dim,breadCrumbLabel,quicklink, measureSelected['locatorText'],"Verify Label")
        checkEqualAssert(dim, str(summary['header']), quicklink, measureSelected['locatorText'], "Verify Summary Header with breadCrumbLabel ")

        checkEqualAssert(str(value_tooltip),value,quicklink, measureSelected['locatorText'], "Tootip Value Validation with PieLegend")
        checkEqualAssert(value,str(summary['data'][(dim, 0, measureSelected['locatorText'])]), quicklink, measureSelected['locatorText'], "Verify Summary Data value with pielegend (All Sub)")
        # Need clarifications on How to calculate PerSub Value
        checkEqualAssert(value, str(summary['data'][(dim, 1, measureSelected['locatorText'])]), quicklink, measureSelected['locatorText'],"Verify Summary Data value with pielegend (Per Sub)")

    return True

def unSetPie(setup,instance):

    instance.piecomponent.setSelection(1, getHandle(setup, MuralConstants.ATSCREEN,"piechart"),True)
    instance.piecomponent.setSelection(1, getHandle(setup, MuralConstants.ATSCREEN,"piechart"),True)

    i = instance.piecomponent.getPieSelections(getHandle(setup, MuralConstants.ATSCREEN,"piechart"))
    j = instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN,"piechart"))

    checkEqualAssert(len(i), len(j['selIndices']), "", "","Verify UnsetPie ")
    return True



def unSetPieLegend(setup, instance):

    instance.pielegend.setSelection(setup.dH, [2], getHandle(setup, MuralConstants.ATSCREEN,"pielegend"),True)
    instance.pielegend.setSelection(setup.dH, [2], getHandle(setup, MuralConstants.ATSCREEN,"pielegend"),True)

    i = instance.piecomponent.getPieSelections(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
    j = instance.pielegend.getSelection(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))

    checkEqualAssert(len(i), len(j['selIndices']), "", "", "Verify UnsetPie ")
    return True

def toolTipPieAndPieLegend(setup,instance):
    p = getHandle(setup, MuralConstants.ATSCREEN,"piechart")
    q = instance.piecomponent.getToolTipInfo(setup, setup.dH,getHandle(setup, MuralConstants.ATSCREEN,"piechart"))
    # print str(q[i].split('\n')[0])
    r = instance.pielegend.getData11(getHandle(setup, MuralConstants.ATSCREEN,"pielegend"))
    # print str(r['legendText'][i].split('\n')[0])
    for i in range(0, len(p['piechart']['arcs'])):
        checkEqualAssert(str(q[i].split('\n')[0]),str(r['legendText'][i].split('\n')[0]),"","","Tootip Text Validation")
        checkEqualAssert(str(q[i].split('\n')[1]),str(r['legendText'][i].split('\n')[1]),"","","Tootip Value Validation")
    return True





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




