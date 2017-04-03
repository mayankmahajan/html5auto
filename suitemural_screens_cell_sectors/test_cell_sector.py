from classes.Components.TimeRangeComponentClass import *
from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
#from classes.Pages.MuralScreens.AccessTechnologyClass import *
from classes.Pages.MuralScreens.CellSectorClass import *
from MuralUtils import ReportsHelper
import sys


screen="Cell Sectors"

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
    networkScreenInstance.cm.goto("Cell Sectors", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    isError(setup)
    cellsectorScreenInstance = CellSectorClass(setup.d)

    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    defaultselectedQuicklink = cellsectorScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.CellSectorScreen, "ktrs"))
    checkEqualAssert("Yesterday",defaultselectedQuicklink,"","","Verify default quicklink value")
    #default_value=getHandle(setup, MuralConstants.SubscriberScreen, 'allinputs')['allinputs']['input'][0].get_attribute("value")
    #checkEqualAssert("1000",str(default_value),defaultselectedQuicklink,"","Verify default number of subscriber")
    #defaulttableheader=getHandle(setup,MuralConstants.SubscriberScreen,"screenarea")['screenarea']['tableheader'][0].text
    #checkEqualAssert("Top 1000 Subscribers by Volume (Downlink)",defaulttableheader,defaultselectedQuicklink,"","Verify default table header")

    for e in quicklink:
        cellsectorScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'], getHandle(setup, MuralConstants.CellSectorScreen, "ktrs"))
        isError(setup)
        selectedQuicklink = cellsectorScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.CellSectorScreen, "ktrs"))

        t = TimeRangeComponentClass().get_Label(e)
        t1 = cellsectorScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.CellSectorScreen, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

        screenName = cellsectorScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.CellSectorScreen, "exploreBar"))
        checkEqualAssert(screen,str(screenName),selectedQuicklink,"","Verify Screen Name")
        #breadCrumbLabel = subscriberScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
        h=getHandle(setup,MuralConstants.CellSectorScreen,'dropdowncontainer')
        ggsn_header = str(h['dropdowncontainer']['label'][0].text)
        sgsn_header = str(h['dropdowncontainer']['label'][1].text)

        checkEqualAssert("GGSN List",ggsn_header,selectedQuicklink,"","Verify GGSN header")
        checkEqualAssert("SGSN List", sgsn_header, selectedQuicklink, "", "Verify SGSN header")

        columns = setup.cM.getNodeElements("cellsectorsorttablecolumn", "column")
        column_names = []
        for k, column in columns.iteritems():
            column_names.append(column['locatorText'])

        ggsn_element=[]
        ggsn_elements=(str(h['dropdowncontainer']['select'][0].text)).split('\n')
        for ele in ggsn_elements:
            if len(ele.strip()):
                ggsn_element.append(ele.strip())

        sgsn_element = []
        sgsn_elements = (str(h['dropdowncontainer']['select'][1].text)).split('\n')
        for ele in sgsn_elements:
            if len(ele.strip()):
                sgsn_element.append(ele.strip())

        for ggsn in ggsn_element:

            ggsnSelected = cellsectorScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.CellSectorScreen, "dropdowncontainer"), str(ggsn), index=0, parent="dropdowncontainer")
            isError(setup)
            checkEqualAssert(ggsn, ggsnSelected, selectedQuicklink,"","Verify Selected GGSN")
            for sgsn in sgsn_element:
                sgsnSelected = cellsectorScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.CellSectorScreen, 'dropdowncontainer'), str(sgsn), index=1,parent='dropdowncontainer')
                isError(setup)
                checkEqualAssert(sgsn, sgsnSelected, selectedQuicklink, "", "Verify Selected SGSN")


                for columnname in column_names:
                    tableHandle = getHandle(setup, MuralConstants.CellSectorScreen, "table")
                    tableMap = cellsectorScreenInstance.table.getTableDataMap(tableHandle, driver=setup, colIndex=-1)

                    if tableMap['rows'] == Constants.NODATA:
                        logger.info("*********No Table Data for GGSN=%s SGSN=%s ************* ", ggsnSelected, sgsnSelected)
                        break

                    sortedData = ReportsHelper.sortTable2(setup, cellsectorScreenInstance, columnName=columnname)
                    # sortedData=subscriberScreenInstance.table.sortTable1(tableHandle, columnname)

                    resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnname)
                    # checkEqualDict(sortedData, tableMap['rows'], "", "", "Checking each row of Table")
                    for k, v in sortedData.iteritems():
                        if tableMap['rows'].has_key(k):
                            checkEqualAssert(tableMap['rows'][k], sortedData[k], selectedQuicklink, "","verify sorted Table rows present in table with key : " + k)
                        else:
                            logger.info("table not contain row with key : " + k)

            setup.d.close()

    setup.d.close()

except Exception as e:
    # print str(e)
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()
