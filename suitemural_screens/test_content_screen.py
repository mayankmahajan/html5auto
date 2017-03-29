from classes.Components.TimeRangeComponentClass import *
from MuralUtils.ContentHelper import *

# new apis

#btv = networkScreenInstance.multibtv.getBTVData(getHandle(setup, MuralConstants.ContentScreen, "btvGroup"))
# setSel = networkScreenInstance.multibtv.setSelection([2,3],getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=1)
# getSel = networkScreenInstance.multibtv.getSelections(getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=1)
#
# tooltipData = networkScreenInstance.multibtv.getToolTipInfo(setup,getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=1)


screen="Content"
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
    networkScreenInstance.cm.goto("Content", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")


    for e in quicklink:

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
                    checkEqualAssert([0],isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify Default Direction Selected for Measure = " + measureSelected)

                    linkSelected = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcherText(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"),occurence=1)
                    checkEqualAssert("Traffic Type",str(linkSelected[0]),selectedQuicklink,measureSelected,"Verify default selected link ")

                    for d in range(0,3):
                        if networkScreenInstance.switcher.measureChangeSwitcher(d,getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection")):
                            selectedSwitcher = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"))
                            checkEqualAssert([d],selectedSwitcher,selectedQuicklink,measureSelected,"Verify Selected Measure Direction")
                            for l in range(0,3):
                                if networkScreenInstance.switcher.measureChangeSwitcher(l,getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"),occurence = 1):
                                    selectedlinkSwitcher = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"),occurence=1)
                                    checkEqualAssert([l], selectedlinkSwitcher, selectedQuicklink, measureSelected,"Verify Selected Measure link")
                                    h = getHandle(setup, MuralConstants.ContentScreen, "general")

                                    for secondmesindex in range(len(h['general']['drop'])):
                                        if len(h['general']['drop']) == 2:
                                            checkEqualAssert([2],selectedlinkSwitcher,selectedQuicklink,measureSelected,"Verify switcher between Service Provider and  Web Protocol present for Web Only")
                                            networkScreenInstance.picker.domultipleSelectionWithIndex_type2(getHandle(setup, MuralConstants.ContentScreen, "general"), secondmesindex, 1,"general", "drop")
                                            isError(setup)
                                            valuefrommes = h['general']['drop'][1].find_elements_by_xpath("./div/*")[0].text
                                            text=str(h['general']['drop'][1].find_elements_by_xpath("./div/*")[0].text).split('>')
                                            btvdata0 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=0)
                                            btvdata1 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=1)
                                            checkEqualAssert(True, str(text[0]).strip() in str(btvdata0['BTVCOLUMN1'][0]), selectedQuicklink, measureSelected, "Verify left side value =%s from dropdowm with left btv" + str(text[0]))
                                            checkEqualAssert(True, str(text[1]).strip() in str(btvdata1['BTVCOLUMN1'][0]), selectedQuicklink, measureSelected, "Verify right side value =%s from dropdowm with right btv" + str(text[1]))



                                        checkAllComponent(setup,networkScreenInstance,selectedQuicklink,measure,False)

                                        #p = networkScreenInstance.btv.getData(getHandle(setup, MuralConstants.NWSCREEN, "btv"))
                                        #for i in range(1,len(p['BTVCOLUMN1'])):
                                        # p = networkScreenInstance.btv.getData(getHandle(setup, MuralConstants.NWSCREEN, "btv"))
                                        #p = networkScreenInstance.multibtv.getBTVData(setup,getHandle(setup, MuralConstants.ContentScreen, "btvGroup"),occurence=0)
                                        #for i in range(6):
                                        btvdata0 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=0)
                                        numberofindex=random.randint(1, len(btvdata0['BTVCOLUMN1']) - 1)
                                        if numberofindex>10:
                                            numberofindex=10
                                        btv0indcies=[]
                                        for j in range(numberofindex):
                                            btv0indcies.append(random.randint(1, len(btvdata0['BTVCOLUMN1']) - 1))

                                        btvdata1 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=1)
                                        numberofindex = random.randint(1, len(btvdata1['BTVCOLUMN1']) - 1)
                                        if numberofindex>10:
                                            numberofindex=10
                                        btv1indcies = []
                                        for j in range(numberofindex):
                                            btv1indcies.append(random.randint(1, len(btvdata1['BTVCOLUMN1'])) - 1)

                                        #checkEqualAssert(str(btvdata1['BTVCOLUMN1'][len(btvdata1['BTVCOLUMN1']) - 1]),"Unidentified", selectedQuicklink, measureSelected,"Verify Unidentified must be at last in btv")
                                        #checkEqualAssert(str(btvdata1['BTVCOLUMN1'][len(btvdata1['BTVCOLUMN1']) - 2]),"Miscellaneous", selectedQuicklink, measureSelected,"Verify Unidentified must be at second last in btv")

                                        doActionsOnContent(networkScreenInstance, setup,btv0indcies,btv1indcies)
                                        # sleep(8)
                                        checkAllComponent(setup, networkScreenInstance, selectedQuicklink,measure,True)

                else:
                    isDirectionsPresent = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"))
                    checkEqualAssert(False, isDirectionsPresent, selectedQuicklink, measure['locatorText'],"Verify presence of Directions for Measure = " + measureSelected)
                    d = None

                    linkSelected = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcherText(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"), occurence=1)
                    checkEqualAssert("Traffic Type", str(linkSelected[0]), selectedQuicklink, measureSelected,"Verify default selected link ")

                    for l in range(0, 3):
                        if networkScreenInstance.switcher.measureChangeSwitcher(l,getHandle(setup,MuralConstants.NWSCREEN,"measureChangeSection"),occurence=1):
                            selectedlinkSwitcher = networkScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.NWSCREEN, "measureChangeSection"), occurence=1)
                            checkEqualAssert([l], selectedlinkSwitcher, selectedQuicklink, measureSelected,"Verify Selected link")
                            h = getHandle(setup, MuralConstants.ContentScreen, "general")
                            for secondmesindex in range(len(h['general']['drop'])):
                                if len(h['general']['drop']) == 2:
                                    checkEqualAssert([2], selectedlinkSwitcher, selectedQuicklink, measureSelected,"Verify switcher between Service Provider and  Web Protocol present for Web Only")
                                    networkScreenInstance.picker.domultipleSelectionWithIndex_type2(getHandle(setup, MuralConstants.ContentScreen, "general"),secondmesindex, 1, "general", "drop")
                                    isError(setup)
                                    valuefrommes = h['general']['drop'][1].find_elements_by_xpath("./div/*")[0].text
                                    text = str(h['general']['drop'][1].find_elements_by_xpath("./div/*")[0].text).split('>')
                                    btvdata0 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=0)
                                    btvdata1 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=1)
                                    checkEqualAssert(True, str(text[0]).strip() in str(btvdata0['BTVCOLUMN1'][0]), selectedQuicklink, measureSelected, "Verify left side value =%s from dropdowm with left btv" + +str(text[0]))
                                    checkEqualAssert(True, str(text[1]).strip() in str(btvdata1['BTVCOLUMN1'][0]), selectedQuicklink, measureSelected, "Verify right side value =%s from dropdowm with right btv" + str(text[1]))

                                checkAllComponent(setup, networkScreenInstance, selectedQuicklink, measure, False)

                                btvdata0 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=0)
                                numberofindex = random.randint(1, len(btvdata0['BTVCOLUMN1']) - 1)
                                if numberofindex > 10:
                                    numberofindex = 10
                                btv0indcies = []
                                for j in range(numberofindex):
                                    btv0indcies.append(random.randint(1, len(btvdata0['BTVCOLUMN1']) - 1))

                                btvdata1 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=1)
                                numberofindex = random.randint(1, len(btvdata1['BTVCOLUMN1']) - 1)
                                if numberofindex > 10:
                                    numberofindex = 10
                                btv1indcies = []
                                for j in range(numberofindex):
                                    btv1indcies.append(random.randint(1, len(btvdata1['BTVCOLUMN1'])) - 1)

                                doActionsOnContent(networkScreenInstance, setup, btv0indcies, btv1indcies)
                                # sleep(8)
                                checkAllComponent(setup, networkScreenInstance, selectedQuicklink, measure, True)

    #toolTip(setup, networkScreenInstance)
    #tooltipData = networkScreenInstance.multibtv.getToolTipInfo(setup, getHandle(setup, MuralConstants.ContentScreen,"btvGroup"), occurence=1)

    tooltipData = networkScreenInstance.multibtv.getToolTipInfo(setup, getHandle(setup, MuralConstants.ContentScreen,"btvGroup"), occurence=1)
    btvdata1 = networkScreenInstance.multibtv.getBTVData(setup, getHandle(setup, MuralConstants.ContentScreen, "btvGroup"), occurence=1)
    for i in range(1, len(btvdata1['BTVCOLUMN1'])):
        checkEqualAssert(str(btvdata1['BTVCOLUMN1'][i]), str(tooltipData[i - 1].split('\n')[0]).strip(), selectedQuicklink, measureSelected, "Verify tooltip text with btv for index= " + str(i))
        checkEqualAssert(str(btvdata1['BTVCOLUMN2'][i]), str(tooltipData[i - 1].split('\n')[1]).split(':')[1].strip(), selectedQuicklink, measureSelected, "Verify tooltip Value with btv for index= " + str(i))

    networkScreenInstance.cm.activate(getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"), child="export")
    networkScreenInstance.cm.goto(MuralConstants.TandMScreen, getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
    setup.d.close()
        #accesstechnologyScreenInstance.cm.gotoScreenViaBreadCrumb("Network",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
        #accesstechnologyScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))
        #accesstechnologyScreenInstance.cm.gotoScreenViaWorkFlowDrop("Trend & Monitoring",getHandle(setup, MuralConstants.NWSCREEN, "breadcrumb"))

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()