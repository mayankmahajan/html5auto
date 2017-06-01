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

#main_chart_value = '2919000000.0'
#compare_chart_value = '2919000000.0'

try:
    setup = SetUp()
    sleep(8)
    login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Trend", getHandle(setup, MuralConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)
    h = getHandle(setup, MuralConstants.TMSCREEN, 'trend-slider')
    TMScreenInstance.quicktrends.clickOnExpandButton(h,setup=setup)

    measures = setup.cM.getNodeElements("measureswithdirection", "measure")
    dimensions = setup.cM.getNodeElements("tmdimension", "dimension")
    mes = []
    mes_count = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])
        mes_count.append(measure['isCount'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])


    selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))

    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"), parent="trend-compare")
    checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink,"","Verify total number of Chart")


    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"), random.randint(0,len(mes)-1), index=0, parent="trend-header")
        isError(setup)
        selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"), random.randint(0,len(dim)-1), index=1, parent="trend-header")
        isError(setup)



    for i in range(6):
        TMScreenInstance.dropdown.customClick(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare")["trend-compare"]["trendchart"][i])
        isError(setup)
        comparechartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"))
        checkEqualAssert(i,comparechartIndex,selectedQuicklink,"","Verify click on compare Chart with index %s"+str(i))

        view = TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"), parent="trend-main")
        checkEqualAssert(int(view[0]), MuralConstants.LineChartIndex, str(selectedQuicklink), "", "Verify view (line chart) after click on compare chart")

        numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"))
        numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare")
        checkEqualAssert(7, numberofmainchart + numberofcomparechart, selectedQuicklink, "","Verify total number of Chart after click on compare chart")

        p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
        compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),parent="trend-compare",indexOfComp=i)
        checkEqualAssert(compareTrend1,p1,selectedQuicklink,"","Verify equal activated dimension on main chart and compare chart")


        main_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MuralConstants.TMSCREEN, "trend-header"))
        compare_chart_value = TMScreenInstance.quicktrends.getHoverText(getHandle(setup, MuralConstants.TMSCREEN, "trend-compare"), parent="trend-compare", index=comparechartIndex)
        checkEqualAssert(compare_chart_value,main_chart_value,selectedQuicklink,"","Verify Main Chart Value with Compare Chart Value")

        measurefrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"), index=0, parent="trend-header")
        measurefromcompare = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"), index=i, parent="trend-compare")
        checkEqualAssert(str(measurefrommain), str(measurefromcompare), str(selectedQuicklink), "", "Verify measure on Main and Comapre Chart")

        dimensionfrommain = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN,"trend-header"), index=1, parent="trend-header")

        dimensionfromcompare = TMScreenInstance.quicktrends.getDimensionFromCompareChart(getHandle(setup, MuralConstants.TMSCREEN,"trend-compare"),index=i)
        checkEqualAssert(str(dimensionfrommain), str(dimensionfromcompare), str(selectedQuicklink), "", "Verify dimension on Main and Comaper Chart")
        TMScreenInstance.switcher.measureChangeSwitcher(MuralConstants.TableViewIndex, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()