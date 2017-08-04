from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper

def measureAndDimensionAfterMapping(timeRangeFromScreen,measureFromScreen,screenTooltipData,tableName=""):
    query={}
    query['measure']=[]
    query['method']=[]
    measures = ConfigManager().getNodeElements("measure_Mapping", "measure")
    for k, measure in measures.iteritems():
        if str(k)==str(measureFromScreen):
            query['measure'].append(measure['backEnd_ID'])
            query['method'].append(measure['method'])


    filters = ConfigManager().getNodeElements("filter_Mapping", "filter")
    for k, filter in filters.iteritems():
        if str(k) in screenTooltipData.keys() and screenTooltipData[k] !=[]:
            query[filter['backEnd_ID']]=screenTooltipData[k]

    timeRange=timeRangeFromScreen.split('to')

    if len(timeRange)==1:
        startTime=str(timeRangeFromScreen).strip()+" 00:00"
        query['starttime']=str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] =str(getepoch(startTime,tOffset=MRXConstants.TIMEZONEOFFSET)+86400)
    else:
        query['starttime'] =str(getepoch(str(timeRange[0]).strip(),tOffset=MRXConstants.TIMEZONEOFFSET))
        query['endtime'] =str(getepoch(str(timeRange[1]).strip(),tOffset=MRXConstants.TIMEZONEOFFSET))

    query['dimension']=['subscriberid']
    query['tableName']=tableName
    return query


try:

    for i in range(0,1):
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
        tableName=quicklink[str(i)]['table']


        expected={}
        expected = UDHelper.setUDPFilters(udScreenInstance, setup, str(i))
        isError(setup)

        # apply global filters
        udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
        isError(setup)

        h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')

        timeRangeFromScreen=str(h['time_measure']['span'][0].text).strip()
        measureFromScreen=str(h['time_measure']['span'][1].text).strip()
        screenTooltipData = UDHelper.getUDPFiltersToolTipData(MRXConstants.UDSCREEN, setup)


        totalDataForValidation=[]
        queryFromUI={}
        dataFromUI={}


        queryFromUI=measureAndDimensionAfterMapping(timeRangeFromScreen,measureFromScreen,screenTooltipData,tableName)

        dataFromUI['data'] = []
        m_data=''
        d_data=''

        tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
        data = udScreenInstance.table.getSelectedRow(tableHandle)

        if data['rows'] == Constants.NODATA:
            pass
        else:
            columnIndex = udScreenInstance.table.getIndexForValueInArray(data['header'],str(measureFromScreen).strip())
            if columnIndex !=-1:
                listOfValueForSelectedMeasure = []
                for rows in data['rows']:
                    listOfValueForSelectedMeasure.append(rows[columnIndex].strip())

                m_data=str(udScreenInstance.table.getValueFromTable(listOfValueForSelectedMeasure,'sum'))

        actualSegmentDetail,textFromSummary=UDHelper.getSummaryDetailAndValidatePresenceOfValidationBox(setup,MRXConstants.UDSCREEN)
        if len(actualSegmentDetail)==3:
            d_data=str(actualSegmentDetail[1])

        dataForValidation=[]
        dataForValidation.append(queryFromUI)
        dataFromUI['data']=[m_data]
        dataForValidation.append(dataFromUI)
        totalDataForValidation.append(dataForValidation)

        queryFromUI_1=deepcopy(queryFromUI)
        dataFromUI_1=deepcopy(dataFromUI)

        dataForValidation=[]
        queryFromUI_1['method']=['distinct_dimension']
        dataForValidation.append(queryFromUI_1)
        dataFromUI_1['data'] = [d_data]
        dataForValidation.append(dataFromUI_1)
        totalDataForValidation.append(dataForValidation)

        setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    #raise e
    setup.d.close()
