from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MuralScreens.AccessTechnologyClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.TrendingMonitoringPageClass import *

import sys


def getTotalActiveLegendValue(list, iscount):
    active_legend_value = []
    for i in range(len(list)):
        if list[i]['state'] == True:
            active_legend_value.append(UnitSystem().getRawValueFromUI(str(list[i]['value']).split('\n')[1].strip()))
    if iscount == 'sum':
        return (str(sum(active_legend_value)))
    elif iscount == 'avg':
        return str(sum(active_legend_value) / float(len(active_legend_value)))
    else:
        return " "

try:
    setup = SetUp()
    sleep(8)
    login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Trend",getHandle(setup,MuralConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    h = getHandle(setup, MuralConstants.TMSCREEN, 'trend-slider')
    TMScreenInstance.quicktrends.clickOnExpandButton(h,setup=setup)
    footerText = str(getHandle(setup, MuralConstants.TMSCREEN, 'footer')['footer']['label'][0].text.split(' ')[4])

    measures = setup.cM.getNodeElements("measureswithdirection", "measure")
    dimensions = setup.cM.getNodeElements("tmdimension", "dimension")
    mes = []
    c=[]
    tableCount = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])
        c.append(measure['isCount'])
        tableCount.append(measure['isCountForTable'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])

    #TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN))
    #TMScreenInstance.switcher.measureChangeSwitcher(1, getHandle(setup, MuralConstants.TMSCREEN,"trend-main"),parent="trend-main")

    #d = TMScreenInstance.table.getTableData1(getHandle(setup,MuralConstants.TMSCREEN,"table"),"table")
    #index = TMScreenInstance.table.getIndexForValueInArray(d['header'], "Volume (Upload)")
    #[e[1] for e in d['rows']]

    #TMScreenInstance.dropdown.customClick(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][2])

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    for e in quicklink:
        TMScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'],getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))
        isError(setup)
        selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))

        t = TimeRangeComponentClass().get_Label(e)
        t1 = TMScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.ATSCREEN, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

        expectedTableLength=BaseComponentClass().getExpectedTableLengthForQuickLink(setup, footerText,t1,qs[e]['locatorText'])
        TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.TableViewIndex, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
        sleep(2)
        data = TMScreenInstance.table.getTableDataMap(getHandle(setup, MuralConstants.TMSCREEN, "table"), driver=setup)

        if data['rows']=='No Data':
            logger.debug('Data not available for quickink =%s',selectedQuicklink)
            continue

        checkEqualAssert(expectedTableLength,len(data['rows']),selectedQuicklink,'','Verify total number of entry in Table')
        TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.LineChartIndex, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

        for m in range(len(mes)):
            selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN, "trend-header"), str(mes[m]), index=0, parent="trend-header")
            isError(setup)
            legendFlag = True
            for d in range(len(dim)):
                selectedDimension=TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"),str(dim[d]), index=1, parent="trend-header")
                isError(setup)

                if selectedDimension in MuralConstants.DimensionListForFlow_Hit:
                    selectedMeasure = selectedMeasure.replace("Flow", "Hit")

                else:
                    selectedMeasure = selectedMeasure.replace("Hit", "Flow")

                numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
                numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"), parent="trend-compare")
                checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink, selectedMeasure, "Verify total number of Chart")
                TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.LineChartIndex,getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
                main_chart_value=TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MuralConstants.TMSCREEN, "trend-header"))
                #main_chart_value =UnitSystem().getRawValueFromUI(main_chart_text)
                if str(main_chart_value)=='':
                    if dim[d]=='None':
                        l1 = []
                    else:
                        l1 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN, "trend-legend"))
                        checkEqualAssert(True,len(l1)<= MuralConstants.Maximum_Trend_Legend,selectedQuicklink,selectedMeasure,"Verify Maximum number of legand")
                    for i in range(len(l1)):
                        p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        c1 = TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))

                        l2 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN, "trend-legend"))
                        p2 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        checkEqualAssert(True, c1 in p1, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension Color = " + c1)

                        chartIndex=TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))

                        compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare", indexOfComp=chartIndex)
                        checkEqualAssert(p2, compareTrend1, selectedQuicklink, selectedMeasure, "Verify equal activated dimension on main chart and compare chart")

                        TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))
                    continue

                comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"))
                compare_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"),parent="trend-compare",index=comparechartIndex)
                #compare_chart_value = UnitSystem().getRawValueFromUI(compare_chart_text)

                TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.TableViewIndex,getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

                #data = TMScreenInstance.table.getTableData1(getHandle(setup, MuralConstants.TMSCREEN, "table"), "table")
                data = TMScreenInstance.table.getTableDataMap(getHandle(setup, MuralConstants.TMSCREEN, "table"),driver=setup)
                print selectedMeasure
                index = TMScreenInstance.table.getIndexForValueInArray1(data['header'], selectedMeasure)
                print index
                if index== -1:
                    logger.error("Column for %s in %s not found", selectedMeasure, selectedDimension)
                    resultlogger.info(" ************Column for %s in %s not found **********************", selectedMeasure, selectedDimension)
                    continue

                else:
                    value_list =[data['rows'][element][index] for element in data['rows']]
                    valueformtable=TMScreenInstance.table.getValueFromTable(value_list,tableCount[m])

                    if 'Avg' in selectedMeasure and valueformtable != " ":
                        valueformtable = UnitSystem().getValueFromRawValue(valueformtable, unitValue=60)
                    elif ("Flows" in selectedMeasure or 'Unique' in selectedMeasure or "Hits" in selectedMeasure) and valueformtable != " ":
                        valueformtable = UnitSystem().getValueFromRawValue(valueformtable, unitValue=1000.0)
                    elif "Bitrate" in selectedMeasure and valueformtable!=" ":
                        valueformtable = UnitSystem().getValueFromRawValue(valueformtable,unitValue=1024.0,unitstring='bps')
                    elif valueformtable!=" ":
                        valueformtable = UnitSystem().getValueFromRawValue(valueformtable, unitValue=1024.0)

                    else:
                        logger.debug('Not able to find value from table')
                        resultlogger.debug('Not able to find value from table')
                        valueformtable='None'

                    if ('Avg' in selectedMeasure) or ('Unique' in selectedMeasure) and dim[d]=='None':
                        pass
                    else:
                        checkEqualValueAssert(valueformtable, str(main_chart_value), selectedQuicklink, selectedMeasure, "Verify Main Chart Value from Table (some limitation in getting value from Table data )")
                        checkEqualValueAssert(valueformtable, compare_chart_value, selectedQuicklink, selectedMeasure, "Verify Compare Chart Value from Table (some limitation in getting value from Table data )")

                    TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.LineChartIndex,getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

                    if dim[d]=='None':
                        l1 = []
                    else:
                        l1 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))
                        checkEqualAssert(True, len(l1)<= MuralConstants.Maximum_Trend_Legend, selectedQuicklink, selectedMeasure,"Verify Maximum number of legand")
                        active_legend_value_before_clicking=getTotalActiveLegendValue(l1,c[m])


                        if 'Avg' in selectedMeasure and active_legend_value_before_clicking!=" ":
                            logger.info("Raw value from active legend before clicking  = %s",active_legend_value_before_clicking)
                            active_legend_value_before_clicking = UnitSystem().getValueFromRawValue(active_legend_value_before_clicking, unitValue=60)

                        elif ("Flows" in selectedMeasure or 'Unique' in selectedMeasure or 'Hits' in selectedMeasure) and active_legend_value_before_clicking!=" ":
                            logger.info("Raw value from active legend before clicking = %s",active_legend_value_before_clicking)
                            active_legend_value_before_clicking = UnitSystem().getValueFromRawValue(active_legend_value_before_clicking, unitValue=1000.0)


                        elif "Bitrate" in selectedMeasure and active_legend_value_before_clicking!=" ":
                            logger.info("Raw value from active legend before clicking  = %s",active_legend_value_before_clicking)
                            active_legend_value_before_clicking = UnitSystem().getValueFromRawValue(active_legend_value_before_clicking, unitValue=1024.0,unitstring='bps')

                        elif active_legend_value_before_clicking!=" ":
                            logger.info("Raw value from active legend before clicking  = %s",active_legend_value_before_clicking)
                            active_legend_value_before_clicking = UnitSystem().getValueFromRawValue(active_legend_value_before_clicking, 1024.0)

                        checkEqualValueAssert(active_legend_value_before_clicking,main_chart_value,selectedQuicklink,selectedMeasure,"Verify value from active legend with main chart value")
                        checkEqualValueAssert(active_legend_value_before_clicking,compare_chart_value,selectedQuicklink,selectedMeasure, "Verify value from active legend with compare chart value")
                        checkEqualValueAssert(valueformtable, active_legend_value_before_clicking, selectedQuicklink, selectedMeasure,"Verify value from active legend with Table")

                        chartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"))
                        measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"), index=chartIndex, parent="trend-compare")
                        checkEqualAssert(selectedMeasure, str(measurefromcompare), str(selectedQuicklink), "","Verify measure on Main and Compare Chart")
                        dimensionfromcompare = TMScreenInstance.quicktrends.getDimensionFromCompareChart(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),index=chartIndex)
                        checkEqualAssert(selectedDimension,str(dimensionfromcompare),str(selectedQuicklink),"","Verify dimension on main and compare chart")

                    if legendFlag or len(l1)==0:
                        legendIteration=len(l1)
                    else:
                        legendIteration=1

                    for i in range(legendIteration):

                        p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        c1 = TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))

                        main_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MuralConstants.TMSCREEN, "trend-header"))
                        #main_chart_value = UnitSystem().getRawValueFromUI(main_chart_text)


                        l2 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN, "trend-legend"))
                        active_legend_value_after_clicking=getTotalActiveLegendValue(l2, c[m])


                        if 'Avg' in selectedMeasure and active_legend_value_after_clicking != " ":
                            logger.info("Raw value from active legend before clicking  = %s",active_legend_value_after_clicking)
                            active_legend_value_after_clicking = UnitSystem().getValueFromRawValue(active_legend_value_after_clicking, unitValue=60)

                        elif ("Flows" in selectedMeasure or 'Unique' in selectedMeasure or 'Hits' in selectedMeasure) and active_legend_value_after_clicking != " ":
                            logger.info("Raw value from active legend after clicking   = %s",active_legend_value_after_clicking)
                            active_legend_value_after_clicking = UnitSystem().getValueFromRawValue(active_legend_value_after_clicking, unitValue=1000.0)

                        elif "Bitrate" in selectedMeasure and active_legend_value_after_clicking != " ":
                            logger.info("Raw value from active legend before clicking  = %s",active_legend_value_after_clicking)
                            active_legend_value_after_clicking = UnitSystem().getValueFromRawValue(active_legend_value_after_clicking, unitValue=1024.0, unitstring='bps')

                        elif active_legend_value_after_clicking != " ":
                            logger.info("Raw value from active legend before clicking   = %s",active_legend_value_after_clicking)
                            active_legend_value_after_clicking = UnitSystem().getValueFromRawValue(active_legend_value_after_clicking, 1024.0)

                        checkEqualValueAssert(active_legend_value_after_clicking, main_chart_value, selectedQuicklink,selectedMeasure, "Verify value from active legend with main chart value")
                        checkEqualAssert(True, c1 in p1, selectedQuicklink, selectedMeasure, "Checking disabled color in previous view. Color = " + c1)

                        p2 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        checkEqualAssert(True, c1 in p1, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension Color = " + c1)
                        #checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        chartIndex=TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))

                        compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare", indexOfComp=chartIndex)
                        checkEqualAssert(p2, compareTrend1, selectedQuicklink, selectedMeasure, "Verify equal activated dimension on main chart and compare chart")

                        TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))
                        legendFlag=False

            selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN, "trend-header"), 'None', index=1, parent="trend-header")
            isError(setup)

    main_chart_dict, compare_chart_dict = TMScreenInstance.quicktrends.hoverOverTicksGetMainAndCompareChartText(setup,getHandle(setup,MuralConstants.TMSCREEN,"trend-main"),MuralConstants.TMSCREEN,active_compare_chart=chartIndex)
    checkEqualDict(main_chart_dict, compare_chart_dict, str(selectedQuicklink), selectedMeasure,"Verify hover text on Main and conpare chart")

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()