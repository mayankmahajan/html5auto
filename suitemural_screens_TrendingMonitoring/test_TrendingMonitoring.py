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

main_chart_value = '2919000000.0'
compare_chart_value='2919000000.0'


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

    measures = setup.cM.getNodeElements("measureswithdirection", "measure")
    dimensions = setup.cM.getNodeElements("tmdimension", "dimension")
    mes = []
    c=[]
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])
        c.append(measure['isCount'])

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


        for m in range(9):
            for d in range(len(dim)):
                selectedMeasure=TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"),str(mes[m]),index=0,parent="trend-header")
                isError(setup)
                selectedDimension=TMScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"),str(dim[d]), index=1, parent="trend-header")
                isError(setup)

                numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
                numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"), parent="trend-compare")
                checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink, selectedMeasure, "Verify total number of Chart")

                TMScreenInstance.switcher.measureChangeSwitcher(1,getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

                data = TMScreenInstance.table.getTableData1(getHandle(setup, MuralConstants.TMSCREEN, "table"), "table")
                print selectedMeasure
                index = TMScreenInstance.table.getIndexForValueInArray1(data['header'], selectedMeasure)
                print index
                if index== -1:
                    logger.error("Column for %s in %s not found", selectedMeasure, selectedDimension)
                    resultlogger.info(" ************Column for %s in %s not found **********************", selectedMeasure, selectedDimension)
                    continue

                else:
                    value_list =[element[index] for element in data['rows']]
                    valueformtable=TMScreenInstance.table.getValueFromTable(value_list,c[m])

                    #actual value from main chart---> Pending
                    checkEqualAssert(valueformtable, main_chart_value, selectedQuicklink, selectedMeasure, "Verify Main Chart Value from Table")

                    # actual value from compare chart---> Pending
                    #comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))
                    checkEqualAssert(valueformtable, main_chart_value, selectedQuicklink, selectedMeasure, "Verify Compare Chart Value from Table")

                    TMScreenInstance.switcher.measureChangeSwitcher(0,getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

                    if dim[d]=='None':
                        l1 = []
                    else:
                        # main chart value --> Pending
                        #compare chart value --> Pending
                        l1 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))
                        active_legend_value_before_clicking=getTotalActiveLegendValue(l1,c[m])
                        checkEqualAssert(active_legend_value_before_clicking,main_chart_value,selectedQuicklink,selectedMeasure,"Verify value from active legend with main chart value")
                        checkEqualAssert(active_legend_value_before_clicking,compare_chart_value,selectedQuicklink,selectedMeasure, "Verify value from active legend with compare chart value")
                        checkEqualAssert(valueformtable, active_legend_value_before_clicking, selectedQuicklink, selectedMeasure,"Verify value from active legend with Table")

                        chartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"))
                        #measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"), index=chartIndex, parent="trend-compare")
                        #checkEqualAssert(selectedMeasure, str(measurefromcompare), str(selectedQuicklink), "","Verify measure on Main and Comapre Chart")

                    for i in range(len(l1)):

                        p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        c1 = TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))

                        #main chart value --> Pending
                        l2 = TMScreenInstance.quicktrends.getLegends_tm(getHandle(setup, MuralConstants.TMSCREEN, "trend-legend"))
                        active_legend_value_after_clicking=getTotalActiveLegendValue(l2, c[m])
                        checkEqualAssert(active_legend_value_after_clicking, main_chart_value, selectedQuicklink,selectedMeasure, "Verify value from active legend with main chart value")


                        checkEqualAssert(True, c1 in p1, selectedQuicklink, selectedMeasure, "Checking disabled color in previous view. Color = " + c1)

                        p2 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
                        checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        checkEqualAssert(True, c1 in p1, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension Color = " + c1)
                        checkEqualAssert(False, p1 == p2, selectedQuicklink, selectedMeasure, "Line Chart should not show deactivated Dimension")
                        chartIndex=TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))

                        compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare", indexOfComp=chartIndex)
                        checkEqualAssert(p2, compareTrend1, selectedQuicklink, selectedMeasure, "Verify equal activated dimension on main chart and compare chart")

                        TMScreenInstance.quicktrends.clickLegendByIndex_tm(i, getHandle(setup, MuralConstants.TMSCREEN,"trend-legend"))

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()