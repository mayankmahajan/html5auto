from MuralUtils.AccessTechnologyHelper import *
from classes.Components.TimeRangeComponentClass import *

screen="Access Technology"
try:
    setup = SetUp()
    sleep(8)
    login(setup,"admin","Admin@123")
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
    networkScreenInstance = NetworkScreenClass(setup.d)
    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)

    #accesstechnologyScreenInstance.cm.activate(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"), child="export")
    #accesstechnologyScreenInstance.cm.goto(MuralConstants.TandMScreen,getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")


    for e in quicklink:
        #print qs[e]['locatorText']
        #for q in quicklink:

        #accesstechnologyScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        #accesstechnologyScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))

        accesstechnologyScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'],getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        selectedQuicklink = networkScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))

        t = TimeRangeComponentClass().get_Label(e)
        t1 = accesstechnologyScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

        screenName = accesstechnologyScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
        checkEqualAssert(screen,str(screenName),selectedQuicklink,"","Verify Screen Name")
        breadCrumbLabel = accesstechnologyScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

        measures = setup.cM.getNodeElements("networkdimeas", "measure")

        for k, measure in measures.iteritems():
            if not measure.has_key("summaryCard"):
                measureSelected = accesstechnologyScreenInstance.picker.domultipleSelectionWithName(getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"),measure['locatorText'],0,"measureChangeSection","measure")
                checkEqualAssert(measure['locatorText'],measureSelected,selectedQuicklink,measure['locatorText'],"Verify Selected measure")

                if measure.has_key("options") and 'direction' in measure['options']:
                    isDirectionsPresent = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                    checkEqualAssert(list,type(isDirectionsPresent), selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)

                    for d in range(0,3):
                        if accesstechnologyScreenInstance.switcher.measureChangeSwitcher(d,getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection")):
                            selectedSwitcher = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection"))
                            checkEqualAssert([d],selectedSwitcher,selectedQuicklink,measure['locatorText'],"Verify Selected Measure Direction")
                            checkAllComponentRelatedToPie(setup,accesstechnologyScreenInstance,selectedQuicklink,measure,0,False)
                            #checkAllComponentRelatedToPie(setup, instance, measureSelected, index, flag)

                            p = accesstechnologyScreenInstance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))
                            for i in range(len(p['legendText'])):
                                accesstechnologyScreenInstance.pielegend.setSelection(setup.dH, [i],getHandle(setup, MuralConstants.ATSCREEN, "pielegend"), True)
                                # sleep(8)
                                checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure,i,True)

                else:
                    isDirectionsPresent = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                    checkEqualAssert(False, isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)
                    d = None
                    checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure, 0,False)

                    p = accesstechnologyScreenInstance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))
                    for i in range(len(p['legendText'])):
                        accesstechnologyScreenInstance.pielegend.setSelection(setup.dH, [i],getHandle(setup, MuralConstants.ATSCREEN,"pielegend"), True)
                        checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure, i, True)

    toolTipPieAndPieLegend(setup, accesstechnologyScreenInstance)
    accesstechnologyScreenInstance.cm.activate(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"), child="export")
    accesstechnologyScreenInstance.cm.goto(MuralConstants.TandMScreen, getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    setup.d.close()
    #accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    #accesstechnologyScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
    #accesstechnologyScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))

except Exception as e:
    raise e
    print str(e)
    # sys._current_frames()
    setup.d.close()
