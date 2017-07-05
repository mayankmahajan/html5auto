from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import os

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")

    newFilterDetails=setup.cM.getNodeElements("specialEditFilter","filter")

    for k, filterDetail in newFilterDetails.iteritems():
        timeRangeFromPopup=''
        measureFromPopup=''
        overWriteFlag=True
        UDHelper.clearFilter(setup,MRXConstants.UDSCREEN)

        ########################################## Apply Filter ########################################################

        SegmentHelper.clickOnfilterIcon(setup,MRXConstants.UDSCREEN,'nofilterIcon')
        timeRangeFromPopup, measureFromPopup = UDHelper.setQuickLink_Measure(setup, udScreenInstance, k)
        expected_filter = {}
        expected_filter = UDHelper.setUDPFilters(udScreenInstance, setup, k)
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)
        #screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)
        udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN,setup)
        checkEqualDict(expected_filter, udpFilterFromScreen, message="Verify Filters Selections",doSortingBeforeCheck=True)


        if filterDetail['filtername'] == 'specialTest_2':
            timeRangeFromPopupFortest_2 = timeRangeFromPopup
            measureFromPopupFortest_2 = measureFromPopup
            udpFilterFromScreenFortest_2=udpFilterFromScreen


        ############################################ Save Filter########################################################

        h=getHandle(setup,MRXConstants.UDSCREEN,'filterArea')
        h['filterArea']['toggleicon'][0].click()
        udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup,MRXConstants.UDSCREEN,'filterArea'),'Save New Filter',0,parent="filterArea", child="multiSelectDropDown")
        filterDetailFromUI,msg=UDHelper.saveNewFilter(setup,MRXConstants.SNFPOPUP,udScreenInstance,filterDetail)
        if filterDetail['button']=='Save':
            expected_detail = [filterDetail['filtername'], filterDetail['default']]
            checkEqualAssert(expected_detail,filterDetailFromUI,message='Verify Entered detail for Save New filter')

        ############################################ Verify new added Filter############################################

        h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
        h['filterArea']['toggleicon'][0].click()
        udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
        UDHelper.verifySaveFilterFromLoadFilter(setup, udScreenInstance, MRXConstants.LFPOPUP,filterDetail)


    h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
    h['filterArea']['toggleicon'][0].click()
    udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
    dict=UDHelper.getLoadFilterList(getHandle(setup,MRXConstants.LFPOPUP))

    flag=True
    for k, filterDetail in newFilterDetails.iteritems():
        if not filterDetail['filtername'] in dict.keys():
            flag=False
            break


    setup.d.close()


    if flag:
        for k, filterDetail in newFilterDetails.iteritems():
            if str(filterDetail['filtername']).strip()=='specialTest_2' and filterDetail['button']=='Save':
                setup = SetUp()
                login(setup, Constants.USERNAME, Constants.PASSWORD)
                udScreenInstance = UDScreenClass(setup.d)
                exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
                udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
                h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
                h['filterArea']['toggleicon'][0].click()
                udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
                UDHelper.editSaveFilter(setup,MRXConstants.LFPOPUP,udScreenInstance,filterDetail,isSpecialScenario=True)
                udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.LFPOPUP, Constants.ALLBUTTONS))
                ######################################### Load Filter ##########################################################

                UDHelper.clearFilter(setup,MRXConstants.UDSCREEN)

                h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
                h['filterArea']['toggleicon'][0].click()
                udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
                UDHelper.loadFilterFormSaveFilter(setup,MRXConstants.LFPOPUP, filterDetail)

                screenHandle=getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
                timeRangeFromScreen = str(screenHandle['time_measure']['span'][0].text).strip()
                measureFromScreen = str(screenHandle['time_measure']['span'][1].text).strip()

                checkEqualAssert(timeRangeFromPopupFortest_2, timeRangeFromScreen,message='After load filter verify timerange value on screen '+msg+' (Rename filter scenario-2)',testcase_id='MKR-1805')
                checkEqualAssert(measureFromPopupFortest_2, measureFromScreen,message='After load filter verify measure value on screen '+msg+' (Rename filter scenario-2)',testcase_id='MKR-1805')
                udpFilterFromScreen_2 = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
                checkEqualDict(udpFilterFromScreenFortest_2, udpFilterFromScreen_2, message="Verify that a user can re-apply any saved filter (Rename filter scenario-2) "+msg,doSortingBeforeCheck=True,testcase_id='MKR-1805')
                setup.d.close()

    newFilterDetails = setup.cM.getNodeElements("specialEditFilter", "filter")
    for k, filterDetail in newFilterDetails.iteritems():
        if filterDetail['button'] == 'Save' and filterDetail['isOverwrite'] == 'True':
            setup = SetUp()
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            udScreenInstance = UDScreenClass(setup.d)
            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            UDHelper.deleteSaveFilter(setup, MRXConstants.LFPOPUP, udScreenInstance, filterDetail)
            setup.d.close()


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
