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
from Utils.MuralConstants import *
from classes.Pages.GenerateReportsPopClass import GenerateReportsPopClass

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
    inputinfo[MuralConstants.STARTTIME] = time[0].datestring
    starttimeEpoch = getepoch(time[0].datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M:%S")
    inputinfo[MuralConstants.ENDTIME] = ''

    # inputinfo[MuralConstants.ENDTIME] = time[1].datestring
    inputinfo['email'] = reportObj.email
    inputinfo['reportname'] = reportObj.reportName+str(rndmNum)

    # temp fix for recurring
    if 'ecurring' in reportType['locatorText']:
        arr1 = ["Daily","Weekly","Monthly"]
        arr2 = [86400,604800,2592000]
        ran = random.randint(0,2)
        reportType['recurringInterval'] = arr1[ran]
        reportType['recurringIntervalValue'] = arr2[ran]
        endtimeEpoch = int(starttimeEpoch) + int(reportType['recurringIntervalValue'])*int(reportType['recurInstances'])
        inputinfo[MuralConstants.ENDTIME] = getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")

    if 'Hourly' in reportType['locatorText']:
        endtimeEpoch = int(starttimeEpoch) + int(3600)*int(reportType['hourIntances'])
        inputinfo[MuralConstants.ENDTIME] = getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")




    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.REPORTSCREEN,"createdialog"))
    reportScreenInstance.launchCreateReport1(setup.d)

    grPopInstance = GenerateReportsPopClass(setup.d)
    grPopInstance.reportspopup.selectRadioButton(inputinfo['reporttype'], getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"radios"), "label")

    # launching TimeRange Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))

    # selecting quicklink
    grPopInstance.reportspopup.selectRadioButton(inputinfo['timerange'], getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"radios"), "label")

    grPopHandle = getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "generateReportDialog")

    if 'week' not in inputinfo['timerange']:
        if MuralConstants.STARTTIME in reportType.keys() and reportType[MuralConstants.STARTTIME] == "True":
            grPopHandle['generateReportDialog'][MuralConstants.STARTTIME][0].click()
            setCalendar(time[0].year, time[0].month, time[0].day, time[0].hour, time[0].min, grPopInstance, setup,MuralConstants.REPORTWIZARDPOPUP)
            grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))

        # print MuralConstants.STARTTIME, str(getInputText(grPopHandle,'generateReportDialog',MuralConstants.STARTTIME))
        if MuralConstants.ENDTIME in reportType.keys() and reportType[MuralConstants.ENDTIME] == "True":
            grPopHandle['generateReportDialog'][MuralConstants.ENDTIME][0].click()
            setCalendar(time[1].year, time[1].month, time[1].day, time[1].hour, time[1].min, grPopInstance, setup,MuralConstants.REPORTWIZARDPOPUP)
            grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))



        # print MuralConstants.ENDTIME, str(getInputText(grPopHandle,'generateReportDialog',MuralConstants.ENDTIME))
        if 'recurringInterval' in reportType.keys() and reportType['recurringInterval'] != "":
            grPopInstance.dropdown.doSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"recurring"),reportType['recurringInterval'],"recurring","dropdowns")

        if 'recurInstances' in reportType.keys() and reportType['recurringInterval'] != "":
            grPopInstance.dropdown.sendkeys_input(reportType['recurInstances'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),1)
            # grPopInstance.dropdown.customSendkeys(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"recurring")['recurring']["instances"],reportType['recurInstances'])

    # getting info from TimeRange Page

    inputinfo[MuralConstants.STARTTIME] = grPopInstance.dropdown.getValue_input(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),0)

    if 'ourly' not in reportType['locatorText'] and 'ecurring' not in reportType['locatorText']:
        inputinfo[MuralConstants.ENDTIME] = grPopInstance.dropdown.getValue_input(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),1)
        endtimeEpoch = getepoch(str(inputinfo[MuralConstants.ENDTIME]),Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M:%S")


    inputinfo["period"] = str(getDateString(starttimeEpoch,Constants.TIMEZONEOFFSET,"%d %b %Y")) +" - "+ str(getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%d %b %Y"))

    # launching Filters Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))


    inputinfo['filters'] = {}
    reportFilters= setup.cM.getNodeElements("reportwizardfilters","filter")

    # for k in reportFilters:
    #     if k in reportType['filters']:

    if 'network' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['network']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
        for i in range(len(reportObj.filters['network'])):
            subfilter = ["Area","Region","Gateway"]

            if reportObj.filters['network'][i] != '':
                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['network'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['network'][i],i)
                # inputinfo['filters'].append(['network',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)])
            inputinfo['filters'][subfilter[i]] = grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)


    if 'apnrat' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['apnrat']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
        for i in range(len(reportObj.filters['apnrat'])):
            radioname= "APN" if i==0 else "Radio Type"
            if reportObj.filters['apnrat'][i] != '':
                grPopInstance.reportspopup.selectRadioButton(radioname, getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"radios"), "label")

                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['apnrat'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),reportObj.filters['apnrat'][i],i)
                # inputinfo['filters'].append(['apnrat',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)])
                inputinfo['filters'][radioname] = grPopInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.REPORTWIZARDPOPUP,"filterPopup"),i)

    if 'subscriber' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['subscriber']['locatorText'],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "alllinks"))
        for i in range(len(reportObj.filters['subscriber'])):
            if reportObj.filters['subscriber'][i] != '':
                grPopInstance.dropdown.clickCheckBox(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allcheckboxes"),0)
                # inputinfo['filters'].append(['subscriber',i,grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),1)])
                inputinfo['filters'][reportFilters['subscriber']['locatorText']] = grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allinputs"),1)


    # launching Review Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))
    reviewPageParams= {}

    grPopHandle = getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "generateReportDialog")
    reviewPageParams['filters'] = grPopInstance.getFiltersAtReviewPage(grPopHandle)


    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],inputinfo['reportname'])
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allcheckboxes"),0)
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allcheckboxes"),1)
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],inputinfo['email'])


    tempArray = [[e.text for e in el.find_elements_by_xpath("*")] for el in grPopHandle['generateReportDialog']['leftBox'][0].find_elements_by_class_name("groupDiv")]


    # reviewPageParams['filters'] = grPopHandle['generateReportDialog']['filters'][0].text

    reviewPageParams['reportname'] = grPopHandle['generateReportDialog']['reportName'][0].get_attribute("value")
    reviewPageParams['email'] = grPopHandle['generateReportDialog']['emailInput'][0].get_attribute("value")
    reviewPageParams[MuralConstants.STARTTIME] = grPopHandle['generateReportDialog'][MuralConstants.STARTTIME][0].get_attribute("value")
    if 'ecurring' in reportType['locatorText']:
        reviewPageParams["instances"] = grPopHandle['generateReportDialog']["instances"][0].get_attribute("value")
    if 'ecurring' not in reportType['locatorText']:
        reviewPageParams[MuralConstants.ENDTIME] = grPopHandle['generateReportDialog'][MuralConstants.ENDTIME][0].get_attribute("value")
    reviewPageParams['reporttype'] = tempArray[1][0].split("\n")[1]
    reviewPageParams['timerange'] = tempArray[2][1]

    logger.debug("Report with info is going to be submitted")
    for k,v in reviewPageParams.iteritems():
        logger.debug("%s :: %s.",k,v)

    grPopInstance.reportspopup.clickButton("Submit",getHandle(setup, MuralConstants.REPORTWIZARDPOPUP, "allbuttons"))
    resultlogger.debug('<br>*********** Logging Results for %s ***********<br><br>',reportType)
    checkEqualDict(inputinfo,reviewPageParams,"","","Checking report Review Page")
    return [inputinfo,reviewPageParams]

def getFiltersInfo(setup,index=0):
    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenInstance.dropdown.customClick(getHandle(setup,MuralConstants.REPORTSCREEN,"table")['table']['info'][index])
    try:
        reportScreenInstance.dropdown.customClick(getHandle(setup,MuralConstants.REPORTSCREEN,"table")['table']['info'][index])
    except:
        pass

    gHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"alert")
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
    # reportScreenInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.REPORTSCREEN,"createdialog"))


    r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Name")
    r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Id")

    data = reportScreenInstance.table.getTableData1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"table")

    actual ={}
    actual['reportname'] = data['rows'][0][1]
    actual['reporttype'] = data['rows'][0][2]
    actual['filters'] = getFiltersInfo(setup)
    # actual['requestedon'] = data['rows'][0][3]
    actual['period'] = data['rows'][0][5]



    for k,v in actual.iteritems():
        checkEqualAssert(request[k],actual[k],"","","Checking Table for Report Created : "+k)

    print data['rows'][0]


def getTableDataMap(setup):
    reportScreenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
    return reportScreenInstance.table.getTableDataMap(tableHandle, "table", setup)

def sortTable(setup,columnName="Name"):

    reportScreenInstance = ReportsModuleClass(setup.d)

    reportScreenInstance.refreshReportTable(setup.d)

    tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")

    #
    # data1 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata1 = reportScreenInstance.table.convertDataToDict(data1)

    reportScreenInstance.table.sortTable1(tableHandle,columnName)

    tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")

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
    # tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
    #
    # data1 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata1 = reportScreenInstance.table.convertDataToDict(data1)
    #
    # reportScreenInstance.table.sortTable1(tableHandle,columnName)
    #
    # tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
    #
    # data2 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata2 = reportScreenInstance.table.convertDataToDict(data2)
    #
    # print cdata1
    # print cdata2
    #
    # resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnName)
    # checkEqualDict(cdata1,cdata2,"","","Checking each row")


def deleteReport(setup,index):

    reportScreenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
    tableData = reportScreenInstance.table.getTableData1(tableHandle)
    tableDataMap = reportScreenInstance.table.convertDataToDict(tableData)
    reportId = reportScreenInstance.table.getColumnValueMap(tableData,index)
    logger.info("Going to delete Report ID %s",reportId)

    reportScreenInstance.dropdown.customClick(tableHandle['table']['delete'][index])
    try:
        reportScreenInstance.dropdown.customClick(getHandle(setup,MuralConstants.REPORTSCREEN,"table")['table']['delete'][index])
    except:
        pass
    gHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"alert")
    logger.debug("Confirming Delete from Pop up")
    try:
        gHandle['alert']['ok'][0].click()
        try:
            gHandle['alert']['ok'][0].click()
        except:
            pass
        tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
        newTableData = reportScreenInstance.table.getTableMap(tableHandle)

        checkEqualAssert(True,newTableData.keys()[0] in tableDataMap.keys(),"","","Check for Delete Table Entry"+str(reportId))
        return True
    except Exception as e:
        logger.error("Exception found while Deleting ReportId %s : %s",reportId,e)
        return e

def downloadReport(setup,index):

    reportScreenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,MuralConstants.REPORTSCREEN,"table")
    tableData = reportScreenInstance.table.getTableData1(tableHandle)
    reportId = reportScreenInstance.table.getColumnValueMap(tableData,index)
    logger.info("Going to Download Report ID %s",reportId)
    try:
        reportScreenInstance.dropdown.customClick(tableHandle['table']['download'][index])
        try:
            reportScreenInstance.dropdown.customClick(getHandle(setup,MuralConstants.REPORTSCREEN,"table")['table']['download'][index])
        except:
            pass
        logger.info("Downloaded Report ID %s",reportId)
        checkEqualAssert(True,True,"","","Check for Download Report"+str(reportId))
        return True
    except Exception as e:
        logger.error("Exception found while Downloading ReportId : %s",reportId)
        checkEqualAssert(True,e,"","","Check for Download Report"+str(reportId))
        return e







