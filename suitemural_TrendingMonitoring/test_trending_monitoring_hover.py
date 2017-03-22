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

try:
    setup = SetUp()
    sleep(4)
    login(setup,"admin","Admin@123")
    wfstart = WorkflowStartComponentClass()
    sleep(4)
    wfstart.launchScreen("Trend",getHandle(setup,MuralConstants.WFSTARTSCREEN))
    TMScreenInstance = TrendingMonitoringPageClass(setup.d)

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
    selectedMeasure = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN), random.randint(0, len(mes) - 1), index=0, parent="trend-header")
    isError(setup)
    selectedDimension = TMScreenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(getHandle(setup, MuralConstants.TMSCREEN), random.randint(0, len(dim) - 1), index=1, parent="trend-header")
    isError(setup)

    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN),parent="trend-compare")
    checkEqualAssert(7,numberofmainchart+numberofcomparechart,str(selectedQuicklink),"","Verify total number of Chart")

    view=TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
    checkEqualAssert(int(view[0]),0, str(selectedQuicklink), "","Verify View ( It should be Line Chart)")

    p1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN))
    chartIndex = TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN))
    compareTrend1 = TMScreenInstance.quicktrends.getPaths(getHandle(setup, MuralConstants.TMSCREEN),parent="trend-compare", indexOfComp=chartIndex)
    checkEqualAssert(p1, compareTrend1, selectedQuicklink, measure,"Verify equal activated dimension on main chart and compare chart")

    hover_data = TMScreenInstance.quicktrends.hoverOverTicks(setup, getHandle(setup, MuralConstants.TMSCREEN),MuralConstants.TMSCREEN)

    TMScreenInstance.switcher.measureChangeSwitcher(1, getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
    data = TMScreenInstance.table.getTableData1(getHandle(setup, MuralConstants.TMSCREEN, "table"), "table")
    measure = TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.TMSCREEN), index=0, parent="trend-header")
    index = TMScreenInstance.table.getIndexForValueInArray1(data['header'], str(measure))
    value_list = [e[index] for e in data['rows']]

    checkEqualAssert(value_list, hover_data, "", measure, "Verify hover data with table data")




    setup.d.close()

except Exception as e:
    raise e
    print str(e)
    setup.d.close()