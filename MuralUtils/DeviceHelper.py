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


def getSelectionsFromDevice(networkScreenInstance, setup, measureSelected,direction=0):
    # get picker 1
    picker1={}
    picker1['dim'] = []
    picker1['value'] = []
    picker2={}
    picker2['dim'] = []
    picker2['value'] = []
    btv={}
    btv['dim'] = []
    btv['value'] = []
    summary={}
    summary['dim'] = []
    summary['value'] = []

    # networkScreenInstance.btv.getAllSelections(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    btvSel = networkScreenInstance.btv.getAllSelections(getHandle(setup,MuralConstants.DeviceScreen,"btv"))
    for i in range(len(btvSel['BTVCOLUMN1'])):
        btv['dim'].append(btvSel['BTVCOLUMN1'][i])
        btv['value'].append(btvSel['BTVCOLUMN2'][i])
    # btv['header'] = networkScreenInstance.btv.getHeader(getHandle(setup,MuralConstants.DeviceScreen,"btv"),0)

    btv_new = networkScreenInstance.btv.merge_dictionaries(btv,networkScreenInstance.btv.calTotal(btv['dim'],btv['value'],measureSelected))
    sumSel,summary['header'] = networkScreenInstance.summarybar.getSelection3(getHandle(setup,MuralConstants.DeviceScreen,"summarybar"),measureSelected,direction=direction)
    summary['dim'] = summary['header']
    summary['value']=[sumSel[summary['dim'],0,measureSelected],
                      sumSel[summary['dim'],1,measureSelected]]

    return btv_new,summary







def checkAllComponent(setup,instance,quicklink,measureSelected,index,flag,direction=0):
    breadCrumbLabel = instance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.DeviceScreen, "exploreBar"))

    if not flag:
        b1,s1=getSelectionsFromDevice(instance, setup, measureSelected['locatorText'],direction)

        checkEqualAssert("All",b1['dim'][0], quicklink, measureSelected['locatorText'], "Verify Default Selection at BTV = ")
        checkEqualAssert("All",s1['dim'], quicklink, measureSelected['locatorText'], "Verify Default Selection at summary = "+s1['header'])
        checkEqualAssert(b1['dim'][0],s1['dim'], quicklink, measureSelected['locatorText'], "Verify Default Selection at summary = "+s1['header'])
        checkEqualAssert(s1['value'][0],b1['totalValue'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, All Sub")
        checkEqualAssert(s1['value'][1],b1['totalValue'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, Per Sub")
        checkEqualAssert(s1['dim'], breadCrumbLabel, quicklink, measureSelected['locatorText'], "Verify BreadCrumb Label")
        checkEqualAssert(s1['dim'], b1['dimSelected'], quicklink, measureSelected['locatorText'], "Verify Summary Label with BTV")
    else:
        b1,s1=getSelectionsFromDevice(instance, setup, measureSelected['locatorText'],direction)
        checkEqualAssert(s1['dim'], b1['dimSelected'], quicklink, measureSelected['locatorText'], "Verify Summary Label with BTV")
        # checkEqualAssert(b1['dim'][0],s1['dim'], quicklink, measureSelected['locatorText'], "Verify Selection at summary = "+s1['header'])
        checkEqualAssert(s1['dim'], breadCrumbLabel, quicklink, measureSelected['locatorText'], "Verify BreadCrumb Label")
        checkEqualAssert(s1['value'][0],b1['totalValue'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, All Sub")
        checkEqualAssert(s1['value'][1],b1['totalValue'],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, Per Sub")

        # checkEqualAssert(s1['value'][0],b1['value'][0],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, All Sub")
        # checkEqualAssert(s1['value'][1],b1['value'][0],quicklink,measureSelected['locatorText'],"Verify Summary Card data with btv, Per Sub")

        # instance.cm.activate(getHandle(setup, MuralConstants.DeviceScreen, "exploreBar"))
        # isError(setup)
        # instance.cm.goto("Access Technology", getHandle(setup, MuralConstants.DeviceScreen, "exploreBar"))
        # isError(setup)
        # globalFilterInstance = GlobalFiltersPopClass(setup.d)
        # actualFilters = getGlobalFiltersFromScreen(MuralConstants.DeviceScreen, globalFilterInstance, setup)
        # for l in range(len(b1['dim'])):
        #     checkEqualAssert(b1['dim'][l],v[l],quicklink,measureSelected['locatorText'],"Verify Previous Screen Selected Dimension   at next Screen")

        # instance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup, MuralConstants.ATSCREEN, "breadcrumb"))
        # instance.cm.gotoScreenViaBreadCrumb("Access Technology",getHandle(setup, MuralConstants.DeviceScreen, "breadcrumb"))
        # isError(setup)

    return True


def toolTip(setup,instance):
    toolTipData = instance.btv.getToolTipInfo(setup.d,setup.dH,getHandle(setup,MuralConstants.DeviceScreen,"btv"))
    btvdata = instance.btv.getData(getHandle(setup,MuralConstants.DeviceScreen,"btv"))
    for i in range(len(toolTipData)):
        checkEqualAssert(str(toolTipData[i].split('\n')[0]),str(btvdata['BTVCOLUMN1'][i]),"","","Tootip Text Validation")
        checkEqualAssert(str(toolTipData[i].split('\n')[1]),str(btvdata['BTVCOLUMN2'][i]),"","","Tootip Value Validation")
    return True


def doActionsOnDevice(networkScreenInstance, setup, index=2,measureSelected="",direction=0):
    # set btvdata
    btv = {}
    networkScreenInstance.btv.setSelection(1,getHandle(setup,MuralConstants.DeviceScreen,"btv"))
    btv['data'] = networkScreenInstance.btv.setSelection(index,getHandle(setup,MuralConstants.DeviceScreen,"btv"))
    # btv['header'] = networkScreenInstance.btv.getHeader(getHandle(setup,MuralConstants.DeviceScreen,"btv"),0)
    # btv['tooltip']  = networkScreenInstance.btv.getToolTipInfo(setup.d,setup.dH,getHandle(setup,MuralConstants.NWSCREEN,"btv"))

    summary = {}
    summary['data'],summary['header'] = networkScreenInstance.summarybar.getSelection3(getHandle(setup,MuralConstants.DeviceScreen,"summarybar"),measureSelected,direction=direction)

    return btv,summary
