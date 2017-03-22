from classes.Components.TimeRangeComponentClass import *
from MuralUtils.NetworkHelper import *

screen="Network Topology"
# try:
setup = SetUp()
sleep(8)
login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
isError(setup)
wfstart = WorkflowStartComponentClass()
sleep(8)
wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
networkScreenInstance = NetworkScreenClass(setup.d)

qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")


for e in quicklink:
    #print qs[e]['locatorText']
    #for q in quicklink:

    #accesstechnologyScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
    #accesstechnologyScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))

    networkScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'],getHandle(setup, MuralConstants.NWSCREEN, "ktrs"))
    selectedQuicklink = networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.NWSCREEN, "ktrs"))

    t = TimeRangeComponentClass().get_Label(e)
    t1 = networkScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.NWSCREEN, "ktrs"))
    checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    checkEqualAssert(screen,str(screenName),selectedQuicklink,"","Verify Screen Name")
    breadCrumbLabel = networkScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    measures = setup.cM.getNodeElements("networkdimeas", "measure")

    for k, measure in measures.iteritems():
        if not measure.has_key("summaryCard"):
            measureSelected = networkScreenInstance.picker.domultipleSelectionWithName(getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"),measure['locatorText'],0,"measureChangeSection","measure")
            isError(setup)
            checkEqualAssert(measure['locatorText'],measureSelected,selectedQuicklink,measure['locatorText'],"Verify Selected measure")

            if measure.has_key("options") and 'direction' in measure['options']:
                isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                checkEqualAssert(list,type(isDirectionsPresent), selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)

                for d in range(0,3):
                    if networkScreenInstance.switcher.measureChangeSwitcher(d,getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection")):
                        selectedSwitcher = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection"))
                        checkEqualAssert([d],selectedSwitcher,selectedQuicklink,measure['locatorText'],"Verify Selected Measure Direction")
                        checkAllComponent(setup,networkScreenInstance,selectedQuicklink,measure,0,False)
                        #checkAllComponent(setup, instance, measureSelected, index, flag)

                        p = networkScreenInstance.btv.getData(getHandle(setup, MuralConstants.NWSCREEN, "btv"))
                        for i in range(1,len(p['BTVCOLUMN1'])):

                            doActionsOnNetwork(networkScreenInstance,setup,i)
                            # sleep(8)
                            checkAllComponent(setup, networkScreenInstance, selectedQuicklink,measure,i,True)

            else:
                isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                checkEqualAssert(False, isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)
                d = None

                ##
                checkAllComponent(setup, networkScreenInstance, selectedQuicklink,measure, 0,False)

                p = networkScreenInstance.btv.getData(getHandle(setup, MuralConstants.NWSCREEN, "btv"))
                for i in range(len(p['BTVCOLUMN1'])):
                    doActionsOnNetwork(networkScreenInstance,setup,i)
                    checkAllComponent(setup, networkScreenInstance, selectedQuicklink,measure, i, True)

toolTip(setup, networkScreenInstance)
networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"), child="export")
networkScreenInstance.cm.goto(MuralConstants.TandMScreen, getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
setup.d.close()
    #accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    #accesstechnologyScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    #accesstechnologyScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))

# except Exception as e:
#     raise e
#     print str(e)
#     sys._current_frames()
    # setup.d.close()
