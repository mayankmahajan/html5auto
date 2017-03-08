from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
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
    return picker1,picker2,btv



try:


    setup = SetUp()
    wfstart = WorkflowStartComponentClass()
    #
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))

    networkScreenInstance = NetworkScreenClass(setup.d)
    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
    breadCrumbLabel = networkScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))

    # timerange iteractions
    networkScreenInstance.timeBar.getLabel(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
    networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
    networkScreenInstance.timeBar.setQuickLink("Today",getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
    selectedQuicklink = networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
    # networkScreenInstance.timeBar.launchCalendar(getHandle(setup,MuralConstants.NWSCREEN,"ktrs"))
    #
    # timeObj = Time()
    # setCalendar(timeObj.year,timeObj.month, timeObj.day, timeObj.hour, timeObj.min, networkScreenInstance, setup,MuralConstants.CREATERULEPOPUP)
    #

    p1={}
    p2={}
    btv={}
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
                    btv[(selectedQuicklink,measureSelected, e)]\
                        =doActionsOnNetwork(networkScreenInstance,setup)

                    # launch
                    networkScreenInstance.cm.activate(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                    networkScreenInstance.cm.goto("",getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))


            else:
                isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"))
                checkEqualAssert(False,isDirectionsPresent,"","","Verify presence of Directions for Measure = "+measureSelected)
                e=None

                # p1[(selectedQuicklink,measureSelected,e)], \
                #     p2[(selectedQuicklink,measureSelected,e)], \
                #     btv[(selectedQuicklink,measureSelected, e)]\
                #         =doActionsOnNetwork(networkScreenInstance,setup)

                networkScreenInstance.cm.activate(getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                networkScreenInstance.cm.goto("Access Technology",getHandle(setup,MuralConstants.NWSCREEN,"exploreBar"))
                networkScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                networkScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))
                networkScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup,MuralConstants.NWSCREEN,"breadcrumb"))


    # summary = networkScreenInstance.summarybar.getSelection1(setup,getHandle(setup,MuralConstants.NWSCREEN,"summarybar"))
    # print selections






    setup.d.close()
except Exception as e:
    print str(e)
    # sys._current_frames()
    setup.d.close()


