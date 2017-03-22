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

    selectedQuicklink = TMScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))
    checkEqualAssert(str(selectedQuicklink), "Yesterday","", "", "verify quicklink ")
    t = TimeRangeComponentClass().get_Label(selectedQuicklink)
    t1 = TMScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.TMSCREEN, "ktrs"))
    checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

    measures = setup.cM.getNodeElements("measureswithdirection", "measure")
    dimensions = setup.cM.getNodeElements("tmdimension", "dimension")
    j = []
    for k, measure in measures.iteritems():
        j.append(measure['locatorText'])

    dim = []
    for k, dimension in dimensions.iteritems():
        dim.append(dimension['locatorText'])


    numberofmainchart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN,"trend-main"))
    numberofcomparechart = TMScreenInstance.quicktrends.getChartsCount(getHandle(setup, MuralConstants.TMSCREEN),parent="trend-compare")

    checkEqualAssert(7,numberofmainchart+numberofcomparechart,str(selectedQuicklink),"","Verify default total number of Chart")

    view=TMScreenInstance.switcher.getMeasureChangeSelectedSwitcher(getHandle(setup, MuralConstants.TMSCREEN, "trend-main"),parent="trend-main")
    checkEqualAssert(int(view[0]),0, str(selectedQuicklink), "","Verify default view")


    h=getHandle(setup, MuralConstants.TMSCREEN)

    measure=TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(h,index=0,parent="trend-header")
    checkEqualAssert(str(measure),"Volume (Downlink)", str(selectedQuicklink), "", "Verify default measure")

    dimension=TMScreenInstance.dropdown.getSelectionOnVisibleDropDown(h,index=1, parent="trend-header")
    checkEqualAssert(str(dimension), "None", str(selectedQuicklink), "", "Verify default dimension")

    chartIndex=TMScreenInstance.quicktrends.getSelectedCompareChartIndex(getHandle(setup, MuralConstants.TMSCREEN))
    checkEqualAssert(int(chartIndex), 0, str(selectedQuicklink), "", "Verify default compare chart")

    setup.d.close()

except Exception as e:
    raise e
    print str(e)
    setup.d.close()