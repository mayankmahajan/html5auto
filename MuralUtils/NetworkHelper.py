from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *
import sys
from classes.Objects.Time import *
import Helper

def doActionsOnNetwork(networkScreenInstance,setup):
    # set picker 1
    picker1={}
    picker1['data'] = networkScreenInstance.picker.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.NWSCREEN,"picker"),[2,4],0,"picker")
    picker1['header'] =  networkScreenInstance.picker.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"picker"),0)



    # set picker 2
    picker2={}
    picker2['data'] = networkScreenInstance.picker.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.NWSCREEN,"picker"),[2,4],1,"picker")
    picker2['header'] =  networkScreenInstance.picker.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"picker"),1)


    # get btvdata
    btv = {}
    btv['data'] = networkScreenInstance.btv.getData(getHandle(setup,MuralConstants.NWSCREEN,"btv"))
    btv['header'] = networkScreenInstance.btv.getHeader(getHandle(setup,MuralConstants.NWSCREEN,"btv"),0)
    btv['tooltip']  = networkScreenInstance.btv.getToolTipInfo(setup.d,setup.dH,getHandle(setup,MuralConstants.NWSCREEN,"btv"))

    summary = {}
    summary['data'],summary['header'] = networkScreenInstance.summarybar.getSelection2(setup,getHandle(setup,MuralConstants.NWSCREEN,"summarybar"))

    return picker1,picker2,btv,summary

def testScreenFunc(setup,networkScreenInstance):
    try:
        # networkScreenInstance = NetworkScreenClass(setup.d)
        screenDetails = {}
        screenDetails['screenName'] = networkScreenInstance.cm.getScreenName(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
        screenDetails['breadCrumbLabel'] = networkScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))

        # timerange iteractions
        quicklinks = {}
        quicklinks[str(networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs")))]=\
            [True,networkScreenInstance.timeBar.getLabel(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))]

        checkEqualAssert("Yesterday",networkScreenInstance.timeBar.getSelectedQuickLink(
                getHandle(setup,MuralConstants.NWSCREEN,"ktrs")),"","","Verify Quicklink Selected")

        print networkScreenInstance.timeBar.setQuickLink("Today",getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))

        quicklinks[str(networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs")))]=\
            [True,networkScreenInstance.timeBar.getLabel(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))]

        selectedQuicklink = networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))

        checkEqualAssert("Today","selectedQuicklink","","","Verify Quicklink Selected")

        # networkScreenInstance.timeBar.launchCalendar(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
        #
        # timeObj = Time()
        # setCalendar(timeObj.year,timeObj.month, timeObj.day, timeObj.hour, timeObj.min, networkScreenInstance, setup,MuralConstants.CREATERULEPOPUP)
        #
        screenDetails['timeRange']={}
        screenDetails['timeRange'][str(networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs")))]=\
            [True,networkScreenInstance.timeBar.getLabel(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))]

        p1={}
        p2={}
        btv={}
        summary = {}

        screenDetails['p1']=p1
        screenDetails['p2']=p2
        screenDetails['btv']=btv
        screenDetails['summary']=summary

        # setting up measures
        measures = setup.cM.getNodeElements("networkdimeas","measure")
        for k,measure in measures.iteritems():
            if not measure.has_key("summaryCard"):
                measureSelected = networkScreenInstance.picker.domultipleSelectionWithName(
                        getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection")
                        ,measure['locatorText'],0,"measureChangeSection","measure")
                checkEqualAssert(measure['locatorText'],measureSelected,"","","Verify Selected measure")
                if measure.has_key("options") and 'direction' in measure['options']:
                    isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(
                        getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                    checkEqualAssert(not False, isDirectionsPresent, "", "",
                                     "Verify presence of Directions for Measure = " + measureSelected)

                    for e in range(3):
                        if networkScreenInstance.switcher.measureChangeSwitcher(e,getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection")):
                            selectedSwitcher = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(
                                    getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"))
                            checkEqualAssert([e],selectedSwitcher,"","","Verify Selected Measure Direction")
                        p1[(selectedQuicklink,measureSelected,e)], \
                        p2[(selectedQuicklink,measureSelected,e)], \
                        btv[(selectedQuicklink,measureSelected, e)], \
                        summary[(selectedQuicklink,measureSelected, e)]\
                            =doActionsOnNetwork(networkScreenInstance,setup)


                        # launch
                        networkScreenInstance.cm.activate(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                        networkScreenInstance.cm.goto("Access Technology",getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                        networkScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                        networkScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                        networkScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))


                else:
                    isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"))
                    checkEqualAssert(False,isDirectionsPresent,"","","Verify presence of Directions for Measure = "+measureSelected)
                    e=None

                    p1[(selectedQuicklink,measureSelected,e)],\
                    p2[(selectedQuicklink,measureSelected,e)],\
                    btv[(selectedQuicklink,measureSelected, e)],\
                    summary[(selectedQuicklink,measureSelected, e)]\
                        =doActionsOnNetwork(networkScreenInstance,setup)


                    networkScreenInstance.cm.activate(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                    networkScreenInstance.cm.goto("Access Technology",getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                    networkScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                    networkScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                    networkScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))


    except Exception as e:
        return e

