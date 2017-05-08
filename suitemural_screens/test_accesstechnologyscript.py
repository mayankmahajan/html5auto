from MuralUtils.AccessTechnologyHelper import *
from classes.Components.TimeRangeComponentClass import *

screen="Access Technology"
try:
    setup = SetUp()
    sleep(8)
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))
    networkScreenInstance = NetworkScreenClass(setup.d)

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    networkScreenInstance.cm.goto("Access Technology", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    isError(setup)
    screenName = networkScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    checkEqualAssert(screen, str(screenName), "", "", "Verify Screen Name after drill from Network Screen")

    accesstechnologyScreenInstance = AccessTechnolohyScreenClass(setup.d)


    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")


    for e in quicklink:
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
                    checkEqualAssert([0], isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify Default Directions for Measure = " + measureSelected)

                    for d in range(0,3):
                        if accesstechnologyScreenInstance.switcher.measureChangeSwitcher(d,getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection")):
                            selectedSwitcher = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.ATSCREEN,"measureChangeSection"))
                            checkEqualAssert([d],selectedSwitcher,selectedQuicklink,measure['locatorText'],"Verify Selected Measure Direction")
                            checkAllComponentRelatedToPie(setup,accesstechnologyScreenInstance,selectedQuicklink,measure,False,d)

                            #unSetPie(setup, accesstechnologyScreenInstance, selectedQuicklink, measure)
                            #need to be fix

                            unSetPieLegend(setup, accesstechnologyScreenInstance, selectedQuicklink, measure)
                            checkTotalSelectionOnPie(setup, accesstechnologyScreenInstance, selectedQuicklink, measure)

                            p = accesstechnologyScreenInstance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))
                            for i in range(len(p['legendText'])):
                                accesstechnologyScreenInstance.pielegend.setSelection(setup.dH, [i],getHandle(setup, MuralConstants.ATSCREEN, "pielegend"), True)
                                checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure,True,d)

                else:
                    isDirectionsPresent = accesstechnologyScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                    checkEqualAssert(False, isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)
                    d = None
                    checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure,False)

                    #unSetPie(setup, accesstechnologyScreenInstance, selectedQuicklink, measure)
                    #need to be fix

                    unSetPieLegend(setup, accesstechnologyScreenInstance, selectedQuicklink, measure)
                    checkTotalSelectionOnPie(setup,accesstechnologyScreenInstance,selectedQuicklink, measure)

                    p = accesstechnologyScreenInstance.pielegend.getData(getHandle(setup, MuralConstants.ATSCREEN, "pielegend"))
                    for i in range(len(p['legendText'])):
                        accesstechnologyScreenInstance.pielegend.setSelection(setup.dH, [i],getHandle(setup, MuralConstants.ATSCREEN,"pielegend"), True)
                        checkAllComponentRelatedToPie(setup, accesstechnologyScreenInstance, selectedQuicklink,measure,True)

    #checkPie(setup,accesstechnologyScreenInstance,selectedQuicklink,measure)
    #need to be fix
    toolTipPieAndPieLegend(setup, accesstechnologyScreenInstance)
    #accesstechnologyScreenInstance.cm.activate(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"), child="export")
    #accesstechnologyScreenInstance.cm.goto(MuralConstants.TandMScreen, getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"), child="export")
    check_click=networkScreenInstance.cm.goto(MuralConstants.ExportToCSV, getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    if check_click==True:
        logger.info("Verify Export to CVS")
    else:
        logger.info("Not able to click on Export to CSV")

    if len(setup.d.window_handles)==2:
        setup.d.switch_to.window(setup.d.window_handles[1])
        setup.d.close()
        setup.d.switch_to.window(setup.d.window_handles[0])

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"), child="export")
    networkScreenInstance.cm.goto(MuralConstants.T_MScreen, getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    setup.d.close()

except Exception as e:
    # print str(e)
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.info("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()
