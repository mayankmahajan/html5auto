from classes.Components.TimeRangeComponentClass import *
from Utils.SetUp import *
from MuralUtils.MuralConstants import *
from Utils.utility import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from classes.Components.WorkflowStartComponent import *
from classes.Components.TimeRangeComponentClass import *
#from classes.Pages.MuralScreens.AccessTechnologyClass import *
from classes.Pages.MuralScreens.SubscriberClass import *
from MuralUtils import Helper
Keys.ENTER

import sys

screen="Top Subscribers"
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
    networkScreenInstance.cm.goto("Top Subscribers", getHandle(setup, MuralConstants.NWSCREEN, "exploreBar"))
    isError(setup)
    subscriberScreenInstance = SubscriberScreenClass(setup.d)


    qs = setup.cM.getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = setup.cM.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

    defaultselectedQuicklink = subscriberScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.SubscriberScreen, "ktrs"))
    checkEqualAssert("Yesterday",defaultselectedQuicklink,"","","Verify default quicklink value")
    default_value=getHandle(setup, MuralConstants.SubscriberScreen, 'allinputs')['allinputs']['input'][0].get_attribute("value")
    checkEqualAssert("1000",str(default_value),defaultselectedQuicklink,"","Verify default number of subscriber")
    defaulttableheader=getHandle(setup,MuralConstants.SubscriberScreen,"screenarea")['screenarea']['tableheader'][0].text
    checkEqualAssert("Top 1000 Subscribers by Volume (Downlink)",defaulttableheader,defaultselectedQuicklink,"","Verify default table header")


    for e in quicklink:
        subscriberScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'], getHandle(setup, MuralConstants.SubscriberScreen, "ktrs"))
        selectedQuicklink = subscriberScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MuralConstants.SubscriberScreen, "ktrs"))

        t = TimeRangeComponentClass().get_Label(e)
        t1 = subscriberScreenInstance.timeBar.getLabel(getHandle(setup, MuralConstants.SubscriberScreen, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

        screenName = subscriberScreenInstance.cm.getScreenName(getHandle(setup, MuralConstants.SubscriberScreen, "exploreBar"))
        checkEqualAssert(screen,str(screenName),selectedQuicklink,"","Verify Screen Name")
        #breadCrumbLabel = subscriberScreenInstance.cm.getRHSBreadCrumbLabel(getHandle(setup, MuralConstants.ATSCREEN, "exploreBar"))
        h=getHandle(setup,MuralConstants.SubscriberScreen,'allinputs')
        #h['allinputs']['input'][0].send_keys(10)

        topsubs = setup.cM.getNodeElements("subscriber", "sub")
        num = []
        for k, topsub in topsubs.iteritems():
            num.append(topsub['value'])

        columns=setup.cM.getNodeElements("subscribersorttablecolumn","column")
        column_names=[]
        for k, column in columns.iteritems():
            column_names.append(column['locatorText'])


        for value in num:
            logger.info("Going to Enter Value = %s",value)
            numberfromscreen=subscriberScreenInstance.cm.sendkeys_input(value,h,0)
            checkEqualAssert(value,str(numberfromscreen),selectedQuicklink,"","Verify number of subscriber with actual number given in config")
            subscriberScreenInstance.cm.sendkeys_input(Keys.ENTER, h, 0,clear=False)
            isError(setup)


            for columnname in column_names:
                tableHandle=getHandle(setup, MuralConstants.SubscriberScreen, "table")
                tableMap=subscriberScreenInstance.table.getTableDataMap(tableHandle,driver=setup,colIndex=-1)

                if tableMap['rows'] == Constants.NODATA:
                    logger.info("No Table Data for Top Subscriber=%s ", value)
                    break

                sortedData = Helper.sortTable(setup,subscriberScreenInstance,columnName=columnname)
                #sortedData=subscriberScreenInstance.table.sortTable1(tableHandle, columnname)

                resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>', columnname)
                #checkEqualDict(sortedData, tableMap['rows'], "", "", "Checking each row of Table")
                for k, v in sortedData.iteritems():
                    if tableMap['rows'].has_key(k):
                        checkEqualAssert(tableMap['rows'][k], sortedData[k], selectedQuicklink, "", "verify sorted Table rows present in table with key : " + k)
                    else:
                        logger.info("********table not contain row with key********* : " + k)

                tableheader = getHandle(setup, MuralConstants.SubscriberScreen, "screenarea")['screenarea']['tableheader'][0].text
                checkEqualAssert("Top "+value+" Subscribers by "+columnname,tableheader,selectedQuicklink,"", "Verify default table header")

    setup.d.close()

except Exception as e:
    # print str(e)
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()

