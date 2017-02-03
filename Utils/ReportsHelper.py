#!/usr/bin/env python
##############################################################
'''
Called Directly from TestCase
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################

from Utils.utility import *

def createreport(setup,reportType,reportObj,time):
    '''
    takes input as reporttype,time,filters,reportName,other optional params
    :return: request and response dictionaries
    '''

    # creating a random number
    rndmNum = random.randint(0,999999)


    inputinfo={}
    inputinfo['reporttype'] = reportType['id']
    inputinfo['timerange'] = reportType['locatorText']
    inputinfo['starttime'] = time[0].datestring
    inputinfo['endtime'] = ''
    # inputinfo['endtime'] = time[1].datestring
    inputinfo['email'] = reportObj.email
    inputinfo['reportname'] = reportObj.reportName+str(rndmNum)

    # temp fix for recurring
    arr1 = ["Daily","Weekly","Monthly"]
    reportType['recurringInterval'] = arr1[random.randint(0,2)]


    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenInstance.switcher.switchTo(1,getHandle(setup,"report_Screen","createdialog"))
    reportScreenInstance.launchCreateReport1(setup.d)

    grPopInstance = GenerateReportsPopClass(setup.d)
    grPopInstance.reportspopup.selectRadioButton(inputinfo['reporttype'], getHandle(setup,"report2_popup","radios"), "label")

    # launching TimeRange Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))

    # selecting quicklink
    grPopInstance.reportspopup.selectRadioButton(inputinfo['timerange'], getHandle(setup,"report2_popup","radios"), "label")

    grPopHandle = getHandle(setup, "report2_popup", "generateReportDialog")

    if 'week' not in inputinfo['timerange']:
        if 'starttime' in reportType.keys() and reportType['starttime'] == "True":
            grPopHandle['generateReportDialog']['starttime'][0].click()
            setCalendar(time[0].year, time[0].month, time[0].day, time[0].hour, time[0].min, grPopInstance, setup,"report2_popup")
            grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, "report2_popup", "allbuttons"))

        # print "starttime", str(getInputText(grPopHandle,'generateReportDialog','starttime'))
        if 'endtime' in reportType.keys() and reportType['endtime'] == "True":
            grPopHandle['generateReportDialog']['endtime'][0].click()
            setCalendar(time[1].year, time[1].month, time[1].day, time[1].hour, time[1].min, grPopInstance, setup,"report2_popup")
            grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, "report2_popup", "allbuttons"))



        # print "endtime", str(getInputText(grPopHandle,'generateReportDialog','endtime'))
        if 'recurringInterval' in reportType.keys() and reportType['recurringInterval'] != "":
            grPopInstance.dropdown.doSelection(getHandle(setup,"report2_popup","recurring"),reportType['recurringInterval'],"recurring","dropdowns")

        if 'recurInstances' in reportType.keys() and reportType['recurringInterval'] != "":
            grPopInstance.dropdown.sendkeys_input(reportType['recurInstances'],getHandle(setup, "report2_popup", "allinputs"),1)
            # grPopInstance.dropdown.customSendkeys(getHandle(setup,"report2_popup","recurring")['recurring']["instances"],reportType['recurInstances'])

    # getting info from TimeRange Page

    inputinfo['starttime'] = grPopInstance.dropdown.getValue_input(getHandle(setup, "report2_popup", "allinputs"),0)

    if 'ourly' not in reportType['locatorText'] and 'ecurring' not in reportType['locatorText']:
        inputinfo['endtime'] = grPopInstance.dropdown.getValue_input(getHandle(setup, "report2_popup", "allinputs"),1)

    # launching Filters Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))


    inputinfo['filters'] = {}
    reportFilters= setup.cM.getNodeElements("reportwizardfilters","filter")

    # for k in reportFilters:
    #     if k in reportType['filters']:

    if 'network' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['network']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['network'])):
            subfilter = ["Area","Region","Gateway"]

            if reportObj.filters['network'][i] != '':
                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['network'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['network'][i],i)
                # inputinfo['filters'].append(['network',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)])
            inputinfo['filters'][subfilter[i]] = grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)


    if 'apnrat' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['apnrat']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['apnrat'])):
            radioname= "APN" if i==0 else "Radio Type"
            if reportObj.filters['apnrat'][i] != '':
                grPopInstance.reportspopup.selectRadioButton(radioname, getHandle(setup,"report2_popup","radios"), "label")

                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['apnrat'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['apnrat'][i],i)
                # inputinfo['filters'].append(['apnrat',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)])
                inputinfo['filters'][radioname] = grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)

    if 'subscriber' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['subscriber']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['subscriber'])):
            if reportObj.filters['subscriber'][i] != '':
                grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),0)
                # inputinfo['filters'].append(['subscriber',i,grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, "report2_popup", "allinputs"),1)])
                inputinfo['filters'][reportFilters['subscriber']['locatorText']] = grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, "report2_popup", "allinputs"),1)


    # launching Review Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))
    reviewPageParams= {}

    grPopHandle = getHandle(setup, "report2_popup", "generateReportDialog")
    reviewPageParams['filters'] = grPopInstance.getFiltersAtReviewPage(grPopHandle)


    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],inputinfo['reportname'])
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),0)
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),1)
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],inputinfo['email'])


    tempArray = [[e.text for e in el.find_elements_by_xpath("*")] for el in grPopHandle['generateReportDialog']['leftBox'][0].find_elements_by_class_name("groupDiv")]


    # reviewPageParams['filters'] = grPopHandle['generateReportDialog']['filters'][0].text

    reviewPageParams['reportname'] = grPopHandle['generateReportDialog']['reportName'][0].get_attribute("value")
    reviewPageParams['email'] = grPopHandle['generateReportDialog']['emailInput'][0].get_attribute("value")
    reviewPageParams['starttime'] = grPopHandle['generateReportDialog']['starttime'][0].get_attribute("value")
    reviewPageParams['endtime'] = grPopHandle['generateReportDialog']['endtime'][0].get_attribute("value")
    reviewPageParams['reporttype'] = tempArray[1][0].split("\n")[1]
    reviewPageParams['timerange'] = tempArray[2][1]

    logger.debug("Report with info is going to be submitted")
    for k,v in reviewPageParams.iteritems():
        logger.debug("%s :: %s.",k,v)

    grPopInstance.reportspopup.clickButton("Submit",getHandle(setup, "report2_popup", "allbuttons"))
    resultlogger.debug('<br>*********** Logging Results for %s ***********<br><br>',reportType)
    checkEqualDict(inputinfo,reviewPageParams,"","","Checking report Review Page")
    return [inputinfo,reviewPageParams]

def getFiltersInfo(setup):
    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenInstance.dropdown.customClick(getHandle(setup,"report_Screen","table")['table']['info'][0])
    try:
        reportScreenInstance.dropdown.customClick(getHandle(setup,"report_Screen","table")['table']['info'][0])
    except:
        pass

    gHandle = getHandle(setup,"report_Screen","alert")
    filtersText = gHandle['alert']['filters'][0].text
    logger.debug("Closing Info Pop up")
    try:
        gHandle['alert']['close'][0].click()
        try:
            gHandle['alert']['close'][0].click()
        except:
            pass
        return reportScreenInstance.dropdown.getFormattedFilters(str(filtersText).strip().split("\n"))
    except Exception as e:
        logger.error("Exception found while closing Info Pop up : %s",e)
        return e


def checkReportTableForCreatedRecord(setup,request):

    reportScreenInstance = ReportsModuleClass(setup.d)
    # reportScreenInstance.switcher.switchTo(1,getHandle(setup,"report_Screen","createdialog"))


    r = reportScreenInstance.table.sortTable1(getHandle(setup,"report_Screen","table"),"Name")
    r = reportScreenInstance.table.sortTable1(getHandle(setup,"report_Screen","table"),"Id")

    data = reportScreenInstance.table.getTableData1(getHandle(setup,"report_Screen","table"),"table")

    actual ={}
    actual['reportname'] = data['rows'][0][1]
    actual['reporttype'] = data['rows'][0][2]
    actual['filters'] = getFiltersInfo(setup)
    # actual['requestedon'] = data['rows'][0][3]
    # actual['period'] = data['rows'][0][4]



    for k,v in actual.iteritems():
        checkEqualAssert(actual[k],request[k],"","","Checking Table for Report Created : "+k)

    print data['rows'][0]


def getTableDataMap(setup):
    reportScreenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,"report_Screen","table")
    return reportScreenInstance.table.getTableDataMap(tableHandle, "table", setup)

def sortTable(setup,columnName="Name"):

    reportScreenInstance = ReportsModuleClass(setup.d)

    reportScreenInstance.refreshReportTable(setup.d)

    tableHandle = getHandle(setup,"report_Screen","table")

    #
    # data1 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata1 = reportScreenInstance.table.convertDataToDict(data1)

    reportScreenInstance.table.sortTable1(tableHandle,columnName)

    tableHandle = getHandle(setup,"report_Screen","table")

    data2 = reportScreenInstance.table.getTableData1(tableHandle)
    columnIndex = reportScreenInstance.table.getIndexForValueInArray(data2['header'],columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col,reverse=True),col,"","","Checking ColumnName Sort : "+columnName)
    logger.info("Sorted")
    cdata2 = reportScreenInstance.table.convertDataToDict(data2)

    # print cdata1
    return cdata2


    # reportScreenInstance = ReportsModuleClass(setup.d)
    #
    # tableHandle = getHandle(setup,"report_Screen","table")
    #
    # data1 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata1 = reportScreenInstance.table.convertDataToDict(data1)
    #
    # reportScreenInstance.table.sortTable1(tableHandle,columnName)
    #
    # tableHandle = getHandle(setup,"report_Screen","table")
    #
    # data2 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata2 = reportScreenInstance.table.convertDataToDict(data2)
    #
    # print cdata1
    # print cdata2
    #
    # resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
    # checkEqualDict(cdata1,cdata2,"","","Checking each row")








