from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
from Utils.AvailableMethod import *
import json

# newFilterDetails = ConfigManager().getNodeElements("savenewfilter", "filter")
# for k, filterDetail in newFilterDetails.iteritems():
#     setup = SetUp()
#     login(setup, Constants.USERNAME, Constants.PASSWORD)
#     exploreScreenInstance = ExplorePageClass(setup.d)
#     exploreHandle = getHandle(setup, "explore_Screen")
#     exploreScreenInstance.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
#     udScreenInstance = UDScreenClass(setup.d)
#     timeRangeFromPopup = ''
#     measureFromPopup = ''


def measureAndDimensionAfterMapping(timeRangeFromScreen,measureFromScreen,screenTooltipData):
    query={}
    query['measure']=[]
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    for k, measure in measures.iteritems():
        if str(k)==str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])


    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] !=[] and screenTooltipData[k] !=['ALL']:
            query[filter['backEnd_ID']]=screenTooltipData[k]

    timeRange=timeRangeFromScreen.split(Constants.TimeRangeSpliter)

    if len(timeRange)==1:
        startTime=str(str(timeRange[0]).strip().split('(')[0]).strip()+" 00:00"
        query['starttime']=str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] =str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
    else:

        if len(str(timeRange[0]).strip().split(' '))==3:
            query['starttime'] =str(getepoch(str(timeRange[0]).strip()+" 00:00",tOffset=MRXConstants.TIMEZONEOFFSET))
        else:
            query['starttime'] = str(getepoch(str(timeRange[0]).strip(), tOffset=MRXConstants.TIMEZONEOFFSET))

        if len(str(str(timeRange[1]).strip().split('(')[0]).strip().split(' ')) == 3:
            query['endtime'] = str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip() + " 00:00", tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
        else:
            query['endtime'] =str(getepoch(str(str(timeRange[1]).strip().split('(')[0]).strip(),tOffset=MRXConstants.TIMEZONEOFFSET))


    query['dimension']=['subscriberid']
    return query


def fireBV(query,method,table_name,data,testcase=''):
    query['method']=method
    query['table_name']=table_name
    query['data']=data
    query['testcase']=testcase
    import time
    query['id']=str(time.time()).split('.')[0]

    logger.info("Going to dump info from UI for Backend Data validation ::" + str(query))
    with open("DumpFile.txt",mode='a') as fs:
        fs.write(json.dumps(query))
        fs.write(" __DONE__" + "\n")

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    actualAvailableQuickLinkList=UDHelper.availableQuickLink(setup,MRXConstants.UDPPOPUP)
    checkEqualAssert(MRXConstants.ExpectedQuickLinkList,actualAvailableQuickLinkList,message='Verify that a user is able to select filter time range as "Last 30 days", "Last 7 Days", "Yesterday", "Last 24 Hours", "Last 4 Hours"," Today" or, from calendar',testcase_id='MKR-1762')

    actualAvailableMeasureList=UDHelper.availableMeasure(setup,MRXConstants.UDPPOPUP,index=0)
    checkEqualAssert(MRXConstants.ExpectedMeasure,actualAvailableMeasureList,message='Verify that a user is able to select available Measure',testcase_id='MKR-1763')

    udpHandle = getHandle(setup, MRXConstants.AvailableFilterList)
    availableFilter = []
    availableFilter.append(str(udpHandle['availablefilter']['option'][0].text))
    availableFilter.append(str(udpHandle['availablefilter']['option'][1].text))

    for dim in udpHandle['filterTab']['dimension']:
        availableFilter.append(str(dim.text))
    checkEqualAssert(MRXConstants.ExpectedFilterOption, availableFilter,message="Verify that on clicking Filter icon User Distribution Parameters window appears with all the possible fields on which filter can be applied",testcase_id='MKR-1759')

    UDHelper.setQuickLink_Measure(setup, udScreenInstance, str('testCalender')) # Check Calender Scenario (Start Time > End Time)
    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER,udpFilterFromScreen, message="Verify that on pressing Cancel button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')


    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(0))
    isError(setup)
    udScreenInstance.clickIcon(getHandle(setup, MRXConstants.UDPPOPUP,'icons'),child='closePopupIcon')
    udpFilterFromScreen = UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
    checkEqualAssert(MRXConstants.NO_FILTER, udpFilterFromScreen,message="Verify that on pressing X button the selections made on User Distribution Parameters, selected filters do not get applied and the page",testcase_id='MKR-1761')

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    expected = {}
    UDHelper.setUDPFilters(udScreenInstance, setup, str('web_domain1'))
    expected = UDHelper.setUDPFilters(udScreenInstance, setup, str('web_domain2'))
    isError(setup)
    udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    udpFilterFromScreen= UDHelper.getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)

    checkEqualDict(expected,udpFilterFromScreen,message="Verify filter after removing web domain value")


    ############################################# For Toggle State ########################################################

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    expectedtoggleState = {}
    expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_NotEqual',toggleStateFlag=True)
    isError(setup)
    click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    if click_Status:
        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
        actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_NotEqual',validateSearch=True)
        isError(setup)

        for k,v in actualtoggleState.iteritems():
            if str(v)!='':
                checkEqualAssert('Equal',str(v),message='Verify that toggle button state should be Equal for Select ALL case :: filter = '+str(k),testcase_id='')
        udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    # UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    # SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    # expectedtoggleState = {}
    # expectedtoggleState = UDHelper.setUDPFilters(udScreenInstance, setup, 'toggle_Equal',toggleStateFlag=True)
    # isError(setup)
    # click_Status=udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
    #
    # if click_Status:
    #     SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
    #     actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, 'toggle_Equal')
    #     isError(setup)
    #     checkEqualDict(expectedtoggleState,actualtoggleState,message='Verify that toggle button should have that same state that you set while applying filters (Select All + Equal)',testcase_id='MKR-3095')
    #     udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

    ####################################################################################################################


    setup.d.close()

    ###################################### Filter Scenario #############################################################

    for i in range(0,MRXConstants.NUMBEROFFILTERSCENARIO):
        setup = SetUp()
        login(setup, Constants.USERNAME, Constants.PASSWORD)
        udScreenInstance = UDScreenClass(setup.d)
        exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
        udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
        time.sleep(3)
        udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))

        timeRangeFromPopup = ''
        measureFromPopup = ''
        UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
        SegmentHelper.clickOnfilterIcon(setup,MRXConstants.UDSCREEN,'nofilterIcon')
        timeRangeFromPopup,measureFromPopup=UDHelper.setQuickLink_Measure(setup,udScreenInstance,str(i))

        ### get table name form XML
        quicklink = setup.cM.getNodeElements("udpScreenFilters", 'quicklink')
        testcase = setup.cM.getNodeElements("udpScreenFilters", "testcase")

        expected={}
        expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(i))
        isError(setup)
        popUpTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDPPOPUP,setup)
        for k in MRXConstants.ListOfFilterContainingTree:
            if expected[k]!=[]:
                checkEqualAssert(expected[k],popUpTooltipData[k],message='Verify Tree selection on UI ( it should be like level 1 > level 2 > level 3 and soon',testcase_id='MKR-3198')
        checkEqualDict(expected,popUpTooltipData,message="Verify Filters Selections On UDP Popup (Functional)",testcase_id=testcase[str(i)]['value'],doSortingBeforeCheck=True)

        # apply global filters
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        response=isError(setup)
        if response[0]:
            setup.d.close()
            continue

        h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
        timeRangeFromScreen=str(h['time_measure']['span'][0].text).strip()
        measureFromScreen=str(h['time_measure']['span'][1].text).strip()
        checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,message='After apply filter verify timerange value on screen')
        checkEqualAssert(measureFromPopup,measureFromScreen,message='After apply filter verify measure value on screen')
        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)

        SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'filterIcon')
        actualtoggleState = UDHelper.getToggleStateForFilters(udScreenInstance, setup, str(i))
        udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))

        filterFromScreenForDV=UDHelper.mapToggleStateWithSelectedFilter(screenTooltipData,actualtoggleState)

        checkEqualDict(expected, screenTooltipData,message="Verify Filters Selections:: After clicking on Apply button the selected filter gets applied (Functional)", doSortingBeforeCheck=True,testcase_id='MKR-1760'+testcase[str(i)]['value'])

        queryFromUI = {}
        m_data = []
        d_data = []

        queryFromUI = measureAndDimensionAfterMapping(timeRangeFromScreen, measureFromScreen, filterFromScreenForDV)

        tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
        udScreenInstance.table.setSpecialSelection(setup.d, [1, 20], Keys.SHIFT, tableHandle)
        data = udScreenInstance.table.getSelectedRow(getHandle(setup, MRXConstants.UDSCREEN, "table"))

        if data['rows'] ==[]:
            h=getHandle(setup, MRXConstants.UDSCREEN, "table")['table']['no_data_msg']
            if len(h)>0:
                msg=str(h[0].text)
                checkEqualAssert(MRXConstants.NODATAMSG,msg,measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
            else:
                checkEqualAssert(MRXConstants.NODATAMSG,'',measure='Verify that the meaningful message should be shown on the Table view when no data is on screen.',testcase_id='MKR-3094')
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)
            resultlogger.info("No Table Data for globalfilter=%s :: Screenshot with name = %s is saved",screenTooltipData, r)

        else:
            columnIndex = udScreenInstance.table.getIndexForValueInArray(data['header'],str(measureFromScreen).strip())
            if columnIndex !=-1:
                listOfValueForSelectedMeasure = []
                for rows in data['rows']:
                    listOfValueForSelectedMeasure.append(rows[columnIndex].strip())

                m_data.append(str(udScreenInstance.table.getValueFromTable(listOfValueForSelectedMeasure,'sum')))


            actualSegmentDetail,textFromSummary=UDHelper.getSummaryDetailAndValidatePresenceOfValidationBox(setup,MRXConstants.UDSCREEN)
            if len(actualSegmentDetail)==3:
                d_data.append(str(actualSegmentDetail[1]))


        fireBV(queryFromUI, AvailableMethod.Aggr_Measure, quicklink[str(i)]['table'], m_data, testcase[str(i)]['value'])
        fireBV(queryFromUI, AvailableMethod.Distinct_Dimension, quicklink[str(i)]['table'], d_data,testcase[str(i)]['value'])

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    #raise e
    setup.d.close()
