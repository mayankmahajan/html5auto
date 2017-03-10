from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *
import sys

from classes.Objects.Time import *

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

def testScreenFunc(setup):
    try:
        networkScreenInstance = NetworkScreenClass(setup.d)
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
            if not hasattr(measure,"summaryCard"):
                measureSelected = networkScreenInstance.picker.domultipleSelectionWithName(
                        getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection")
                        ,measure['locatorText'],0,"measureChangeSection","measure")
                checkEqualAssert(measure['locatorText'],measureSelected,"","","Verify Selected measure")
                if hasattr(measure,"options") and 'direction' in measure['options']:
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









def setGlobalFilters(setup):
    globalFilterInstance = GlobalFiltersPopClass(setup.d)

    global_network= setup.cM.getNodeElements("globalScreenFilters","network")
    global_apnrat= setup.cM.getNodeElements("globalScreenFilters","apnrat")
    global_device= setup.cM.getNodeElements("globalScreenFilters","device")



    print global_apnrat

    #
    # # for k in reportFilters:
    # #     if k in reportType['filters']:
    #
    # if 'network' in reportType['filters']:
    #     grPopInstance.clickLink(reportFilters['network']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
    #     for i in range(len(reportObj.filters['network'])):
    #         subfilter = ["Area","Region","Gateway"]
    #
    #         if reportObj.filters['network'][i] != '':
    #             # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['network'][i],i)
    #             handle = getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup")
    #             # grPopInstance.multiDropdown.domultipleSelectionWithIndex(handle,[0],i)
    #             grPopInstance.multiDropdown.domultipleSelectionWithIndex(handle,reportObj.filters['network'][i],i)
    #             # inputinfo['filters'].append(['network',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)])
    #         inputinfo['filters'][subfilter[i]] = grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)
    #
    #
    # if 'apnrat' in reportType['filters']:
    #     grPopInstance.clickLink(reportFilters['apnrat']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
    #     for i in range(len(reportObj.filters['apnrat'])):
    #         radioname= "APN" if i==0 else "Radio Type"
    #         if reportObj.filters['apnrat'][i] != '':
    #             grPopInstance.dropdown.clickCheckBox(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allcheckboxes"),0)
    #             grPopInstance.reportspopup.selectRadioButton(radioname, getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"radios"), "label")
    #
    #             # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['apnrat'][i],i)
    #             grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['apnrat'][i],i)
    #             # inputinfo['filters'].append(['apnrat',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)])
    #             inputinfo['filters'][radioname] = grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)
    #
    # if 'subscriber' in reportType['filters']:
    #     linkText = grPopInstance.clickLinkByPartialText(reportFilters['subscriber']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
    #     # linkText = grPopInstance.clickLinkByIndex(2,getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, MuralConstants.ALLLINKS))
    #     for i in range(len(reportObj.filters['subscriber'])):
    #         if reportObj.filters['subscriber'][i] != '':
    #             grPopInstance.dropdown.clickCheckBox(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, MuralConstants.ALLCHECKBOXES),0)
    #             # inputinfo['filters'].append(['subscriber',i,grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),1)])
    #             inputinfo['filters'][linkText] = grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),0)
    #
    # return inputinfo['filters']