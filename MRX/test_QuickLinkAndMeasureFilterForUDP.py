from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")

    measures = setup.cM.getNodeElements("ud_measures", "measure")
    mes = []
    for k, measure in measures.iteritems():
        mes.append(measure['locatorText'])

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")


    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
    flag=True

    for m in range(len(mes)):
        chartAndTableFlag=True
        selectedMeasure = udScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDPPOPUP, "allselects"), str(mes[m]), index=0, parent="allselects")
        for e in quicklink:
            udScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'], getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
            isError(setup)
            selectedQuicklink = udScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
            t1 = udScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))

            if flag:
                t = TimeRangeComponentClass().get_Label(e)
                checkEqualAssert(t[1], t1, selectedQuicklink, selectedMeasure, message="Verify quicklink label")

            timeRangeFromPopup = str(t1 + " (" + selectedQuicklink.strip() + ")").strip()
            measureFromPopup = str(selectedMeasure).strip()

            udScreenInstance.clickButton("Apply", getHandle(setup, MRXConstants.UDPPOPUP, MuralConstants.ALLBUTTONS))
            isError(setup)

            h = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
            timeRangeFromScreen = str(h['time_measure']['span'][0].text).strip()
            measureFromScreen = str(h['time_measure']['span'][1].text).strip()

            checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,selectedQuicklink,selectedMeasure,message='Verify Selected Quicklink applied successfully')
            checkEqualAssert(measureFromPopup,measureFromScreen,selectedQuicklink,selectedMeasure,message='Verify Selected Measure applied successfully')
            testidForChart,testidForGrid = UDHelper.getTestCaseID(selectedMeasure)

            Data_label = str(getHandle(setup, MRXConstants.UDSCREEN, 'body')['body']['data_label'][0].text).strip()
            if Data_label == Constants.NODATA:
                checkEqualAssert(False, True, selectedQuicklink, selectedMeasure,message="Verify Chart and Grid gets plotted for selected measure and quicklink",testcase_id=testidForChart + "," + testidForGrid)
            else:
                if len(getHandle(setup,MRXConstants.UDSCREEN,'body')['body']['lineChartComponent'])>0:
                    if chartAndTableFlag:
                        xAxisPointList=UDHelper.getAxisPoint(getHandle(setup,MRXConstants.UDSCREEN,'body'))
                        UDHelper.validateRangeInChart(xAxisPointList, selectedQuicklink, selectedMeasure)
                    chartPlotted=True
                else:
                    chartPlotted=False

                checkEqualAssert(True,chartPlotted,selectedQuicklink,selectedMeasure,message="Verify that on selecting " +str(selectedMeasure)+" metric for "+ selectedQuicklink+" time range the user distribution chart gets plotted for this metric",testcase_id=testidForChart)
                udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
                time.sleep(2)
                expectedHeader=['Range','Users','% of '+selectedMeasure,selectedMeasure,'Average '+selectedMeasure]
                tableHandle = getHandle(setup, MRXConstants.UDSCREEN, "table")
                data = udScreenInstance.table.getTableData1(tableHandle, "table", length=20)
                checkEqualAssert(expectedHeader,data['header'],selectedQuicklink,selectedMeasure,message="Verify that on selecting " +str(selectedMeasure)+" metric for "+ selectedQuicklink+" time range the user distribution Grid gets plotted for this metric",testcase_id=testidForGrid)
                if chartAndTableFlag:
                    UDHelper.validateRangeAndSortingInTable(udScreenInstance,data,selectedQuicklink,selectedMeasure)

                udScreenInstance.switcher.measureChangeSwitcher_UD(0,getHandle(setup, MRXConstants.UDSCREEN, "switcher"))

            SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')
            chartAndTableFlag=False
        flag=False
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
