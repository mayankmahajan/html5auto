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

from classes.Objects import CreateAlert
from Utils.utility import *
from classes.Pages.GenerateReportsPopClass import GenerateReportsPopClass
from MuralConstants import *
import re
from classes.Objects.Time import *
from classes.Components.AlertsComponentClass import *


def createDPIAlert(setup, request = {}):

    response = {}

    # creating a random number
    rndmNum = random.randint(0,999999)
    popInstance = GenerateReportsPopClass(setup.d)

    # Launching Settings Page

    popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
    popInstance.dropdown.customClick(getHandle(setup,MuralConstants.ALERTSCREEN,"settings")['settings']['createrule'])


    # request = {}
    request['ruleName'] = request['ruleName']+str(rndmNum)
    response['ruleName'] = setName(request['ruleName'],getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS))
    #
    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
    response['measure'] = setDrop(request['measure']['locatorText'],0,allselects)
    response['type'] = setDrop(request['type'],1,allselects)
    response['gran'] = setDrop(request['gran'],2,allselects)
    #
    #
    response['conditions'] = []
    response['conditions'].append(setDPICondition(0,request['conditions'][0],getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup))
    response['conditions'].append(setDPICondition(1,request['conditions'][1],getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup))
    response['conditions'].append(setDPICondition(2,request['conditions'][2],getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup))
    response[MuralConstants.STARTTIME]=setTime(setup,0,request['time'][0])
    starttimeEpoch = getepoch(request['time'][0].datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")

    request['time'][1]= getEndtime(setup, response['type'], response['gran'], starttimeEpoch,Constants.TIMEZONEOFFSET)

    response[MuralConstants.ENDTIME] = setTime(setup,1,request['time'][1])
    #
    # starttimeEpoch = getepoch(request['time'][0].datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M:%S")
    endtimeEpoch = getepoch(request['time'][1].datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")
    # request["range"] = str(getDateString(starttimeEpoch,Constants.TIMEZONEOFFSET,"%a %b %d %Y")) +" to "+ str(getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%a %b %d %Y"))
    request["range"] = str(request['time'][0].datestring) +" to "+ str(request['time'][1].datestring)

    response['filters'] = ""
    for i in range(len(request['filters'])):
        response['filters'] = response['filters']+setFilters(setup,request['filters'][i])+','
        if i < len(request['filters'])-1:
            clickButton(setup,"add",True)
    response['filters']=response['filters'].strip(',')
    request['filters']=response['filters']
    request['measure']=response['measure']
    # filterSelected = setFilters(setup,["Device","Apple iPod"])
    # clickButton(setup,"add")
    # filterSelected = setFilters(setup,["Gateway","gurgaon"])
    clickButton(setup,"Create")

    error = isError(setup)
    if error[0]:
        checkEqualAssert(True,False,"","",str(error[1])+" - Request "+ str(request) +" - Response "+str(response))
        err = str(error[0])+" "+str(error[1])+" "+str(request)+" "+str(response)
        logger.error("ERROR POP UP comes up on creating new Alert = %s",err)
        return error[0],error[1],request,response
    else:
        checkEqualDict(request,response,"","","Comparing alertInputs with Info from AlertDialog")

    checkDPIAlertTableForCreatedRecord(setup,request)

    print "DONE"

def createKPIAlert(setup, request = {}):
    response = {}

    # creating a random number
    rndmNum = random.randint(0,999999)
    popInstance = GenerateReportsPopClass(setup.d)

    # Launching Settings Page
    popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
    popInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.ALERTSCREEN,"settings"),"settings")
    popInstance.dropdown.customClick(getHandle(setup,MuralConstants.ALERTSCREEN,"settings")['settings']['createrule'])

    rulename = "automationrule"+str(rndmNum)
    request['ruleName'] = setName(rulename,getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS))
    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
    # request['gateway'] = setDropRandomly(0, allselects)
    # request['schema'] = setDropRandomly(1, allselects)
    # request['kpi'] = setDropRandomly(2, allselects)
    request['gateway'] = setDrop("Mumbai",0, allselects)
    request['schema'] = setDrop("apn",1, allselects)
    request['kpi'] = setDrop("Packet Drop",2, allselects)

    request['index'] = setDropRandomly(3, allselects)
    request['gran'] = setDropRandomly(4, allselects)

    request['conditions'] = []
    request['conditions'].append(setKPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(1,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(2,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(3,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))

    request['status'] = "Active"
    clickButton(setup,"Create")

    checkKPIAlertTableForCreatedRecord(setup,request)

def checkDPIAlerts(setup):
    popInstance = GenerateReportsPopClass(setup.d)
    # Launching Settings Page
    popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
    # alertRuleMap = {}
    alertRuleMap= getTableDataMap(setup, MuralConstants.ALERTSCREEN)
    popInstance.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
    screenInstance = AlertsComponentClass()
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    checkAlertsPresent(setup,alertRuleMap,alertlist)

def checkAlertsPresent(setup,alertRuleMap,alertlist):
    for i in range(len(alertlist)):
        screenInstance = AlertsComponentClass()
        screenInstance.selectAlert(i,getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"))
        alertFullBody = screenInstance.getAlertFullBody(getHandle(setup,MuralConstants.ALERTSCREEN,"alertinfo"))

        request = merge_dictionaries(alertlist[i],getDPIAlertsDataAsDict(alertRuleMap['rows'][alertFullBody['ruleName']]))
        resultlogger.info("**** Logging results for Alert List and Alert Main Body checks ****")
        resultlogger.info("Expected : %s \n",str(request))
        resultlogger.info("Actual : %s \n", str(alertFullBody))
        for k, v in request.iteritems():
            checkEqualAssert(request[k], alertFullBody[k], "", "", "Checking DPI Alerts : " + k)

def getDPIAlertsDataAsDict(row):
    d={}
    d['ruleName'] = row[0]
    d['gran'] = row[1]
    d['filters'] = row[2]
    d['measure'] = row[3]
    d['conditions'] = [row[4], row[5], row[6]]
    d['range'] = row[7]
    #d['status'] = row[8]
    return d
def getKPIAlertsDataAsDict(row):
    d={}
    d['ruleName'] = row[0]
    d['schema'] = row[1]
    d['kpi'] = row[2]
    d['index'] = row[3]
    d['conditions'] = [row[4],row[5],row[6],row[7]]
    d['status'] = row[8]
    #d['status'] = row[8]
    return d

def getEndtime(setup, type, gran, starttimeEpoch,timezone):
    epoch = calculateEndtimeEpoch(setup,type,gran,starttimeEpoch)
    return createTimeFromEpoch(epoch,timezone)

def calculateEndtimeEpoch(setup, type, gran, starttimeEpoch):
    ran = random.randint(2,3)
    if type == setup.cM.getAllNodeElements("measuretypes","type")[0]:
        if gran == "Hourly":
            return int(starttimeEpoch) + int(ran)*3600
        if gran == "Daily":
            return int(starttimeEpoch) + int(ran)*86400
        if gran == "Monthly":
            return int(starttimeEpoch) + int(ran)*2592000
    else:
        if gran == "Monthly":
            return int(starttimeEpoch) + ((3*30*24)+random.randint(1,(3*24)))*3600
        else:
            return int(starttimeEpoch) + ((21*24)+random.randint(1,(3*24)))*3600
    return int(starttimeEpoch) + int(ran)*2592000

def createTimeFromEpoch(epoch,timezone):
    pattern = "%Y-%m-%d-%H-%M"
    parts=getDateString(epoch,timezone,pattern).split("-")
    return Time(parts[0],parts[1],parts[2],parts[3])

     # = getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%Y-%m-%d-%H-%M")

def checkDPIAlertTableForCreatedRecord(setup,request,index=0):
    # saving the table data as keys
    tableMap = getTableDataMap(setup,MuralConstants.ALERTSCREEN)

    # reportScreenInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.REPORTSCREEN,"createdialog"))
    # r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Name")
    # r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Id")
    # data = reportScreenInstance.table.getTableData1(getHandle(setup,MuralConstants.ALERTSCREEN,"table"),"table")
    row = tableMap['rows'][request['ruleName']]
    print row
    actual = getDPIAlertsDataAsDict(row)

    # actual['ruleName'] = data['rows'][index][0]
    # actual['gran'] = data['rows'][index][1]
    # actual['filters'] = data['rows'][index][2]
    # actual['measure'] = data['rows'][index][3]
    # actual['conditions'] = [data['rows'][index][4],data['rows'][index][5],data['rows'][index][6]]
    # actual['range'] = data['rows'][index][7]
    # actual['status'] = data['rows'][index][8]

    for k,v in actual.iteritems():
        checkEqualAssert(request[k],actual[k],"","","Checking Table for DPI Alert Rule Created : "+k)

    # print data['rows'][0]

def checkKPIAlertTableForCreatedRecord(setup,request,index=0):
    # saving the table data as keys
    tableMap = getTableDataMap(setup,MuralConstants.ALERTSCREEN)
    row = tableMap['rows'][request['ruleName']]
    print row
    actual = getKPIAlertsDataAsDict(row)
    logger.info("Requested Parameters to create KPI Alert = %s",str(request))
    logger.info("Actual Parameters shown in Table for KPI Alerts = %s",str(actual))
    for k,v in actual.iteritems():
        checkEqualAssert(request[k],actual[k],"","","Checking Table for KPI Alert Rule Created : "+k)

def setName(name,handle,index=0):
    instance = DropdownComponentClass()
    return instance.sendkeys_input(name,handle,index)

def setDropRandomly(index, handle):
    instance = DropdownComponentClass()
    return instance.doRandomSelectionOnVisibleDropDown(handle,index)

def setDrop(value,index,handle,selectionByIndex=False):
    instance = DropdownComponentClass()
    if selectionByIndex:
        return instance.doSelectionOnVisibleDropDownByIndex(handle,value,index)
    else:
        return instance.doSelectionOnVisibleDropDown(handle,value,index)

def setDPICondition(priorty, cond, handle, setup,firstDrop=3,enableCondition="",thresholdValue="NA"):

    # operator=re.findall('[=<>]+',cond)
    # number_value=re.findall(r'\d+',cond)
    # unitSystem=re.findall('[a-zA-Z]+',cond)
    #
    # operator=cond[0]
    # number_value=cond[1]
    # unitSystem=cond[2]

    operator=re.findall('[=<>]+',cond)[0]
    number_value=re.findall(r'\d+',cond)[0]
    if thresholdValue != "NA":
            number_value = thresholdValue

    try:
        unitSystem=re.findall('[a-zA-Z]+',cond)[0]
        if priorty==0:
            index = firstDrop
        elif priorty==1:
            index = firstDrop+2
        elif priorty==2:
            index = firstDrop+4

    except:
        unitSystem = ''
        if priorty==0:
            index = firstDrop
        elif priorty==1:
            index = firstDrop+1
        elif priorty==2:
            index = firstDrop+2


    try:
        instance = DropdownComponentClass()

        logger.info("Enabling Priority %s",str(priorty))
        instance.clickCheckBox(handle,priorty)
        logger.info("Priority %s is selected",str(priorty))

        handle = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)

        logger.info("Selecting operator %s for Priority %s",str(operator),str(priorty))
        op=instance.doSelectionOnVisibleDropDown(handle,operator,index)
        logger.info("Operator %s for Priority %s is selected",str(operator),str(priorty))

        # handling a minor UI bug

        logger.info("Entering value %s for operator %s and Priority %s",str(number_value),str(operator),str(priorty))

        if priorty == 2:
            num_value = instance.sendkeys_input(number_value, getHandle(setup,MuralConstants.CREATERULEPOPUP,"allinputs"),0,"allinputs","number")
        else:
            num_value = instance.sendkeys_input(number_value, getHandle(setup,MuralConstants.CREATERULEPOPUP,"allinputs"),priorty+1,"allinputs")

        logger.info("Value %s set for operator %s and Priority %s",str(num_value),str(operator),str(priorty))

        if unitSystem == '':
            returnValue = str(op).strip()+str(num_value).strip()
        else:
            logger.info("Selecting unitsystem %s for operator %s and Priority %s",str(unitSystem),str(operator),str(priorty))
            unit=instance.doSelectionOnVisibleDropDown(handle,unitSystem,index+1)
            logger.info("Unitsystem %s is set for operator %s and Priority %s",str(unitSystem),str(operator),str(priorty))
            returnValue = str(op).strip()+str(num_value).strip()+str(unit).strip()

        if enableCondition == "":
            enableCondition = random.choice([True, False])
        else:
            if not enableCondition:
                instance.clickCheckBox(getHandle(setup,MuralConstants.CREATERULEPOPUP,MuralConstants.ALLCHECKBOXES),priorty)
            return returnValue

        if enableCondition:
            return returnValue
        else:
            logger.info("Disabling Priority %s",str(priorty))
            instance.clickCheckBox(getHandle(setup,MuralConstants.CREATERULEPOPUP,MuralConstants.ALLCHECKBOXES),priorty)
            logger.info("Priority %s is Disabled",str(priorty))
            return "-"



    except Exception as e:
        logger.error("Exception found while setting condition at CreateRule for DPI [Priority: %s, Operator: %s, Value: %s, Unit: %s  =  %s",
                     str(priorty),str(operator),str(number_value),str(unitSystem), str(e) )
        return e

def setKPICondition(priorty, handle, setup,firstDrop=3,enableCondition="",thresholdValue="NA"):
    if priorty==0:
        index = firstDrop
    elif priorty==1:
        index = firstDrop+1
    elif priorty==2:
        index = firstDrop+2
    elif priorty==3:
        index = firstDrop+3

    if thresholdValue == "NA":
            thresholdValue = random.randint(0,100)



    try:
        instance = DropdownComponentClass()
        logger.info("Enabling Priority %s",str(priorty))
        instance.clickCheckBox(handle,priorty)
        logger.info("Priority %s is selected",str(priorty))
        handle = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
        op=instance.doRandomSelectionOnVisibleDropDown(handle,index)
        logger.info("Operator %s for Priority %s is selected",str(op),str(priorty))
        num_value = instance.sendkeys_input(thresholdValue, getHandle(setup,MuralConstants.CREATERULEPOPUP,"allinputs"),priorty+1,"allinputs")
        logger.info("Value %s set for operator %s and Priority %s",str(num_value),str(op),str(priorty))

        if enableCondition == "":
            enableCondition = random.choice([True, False])
        else:
            if not enableCondition:
                instance.clickCheckBox(getHandle(setup,MuralConstants.CREATERULEPOPUP,MuralConstants.ALLCHECKBOXES),priorty)
            return str(op).strip()+str(num_value).strip()


        if enableCondition:
            return str(op).strip()+str(num_value).strip()
        else:
            # if random.choice([True, False]):
            #     return str(op).strip()+str(num_value).strip()
            # else:
            logger.info("Disabling Priority %s",str(priorty))
            instance.clickCheckBox(getHandle(setup,MuralConstants.CREATERULEPOPUP,MuralConstants.ALLCHECKBOXES),priorty)
            logger.info("Priority %s is Disabled",str(priorty))
            return "-"

    except Exception as e:
        logger.error("Exception found while setting condition at CreateRule for KPI [Priority: %s, Operator: %s, Value: %s  =  %s",
                     str(priorty),str(op),str(num_value), str(e) )
        return e

def setTime(setup,startEnd,timeObj):
    instance = GenerateReportsPopClass(setup.d)
    handle = getHandle(setup,MuralConstants.CREATERULEPOPUP)

    t = MuralConstants.STARTTIME if startEnd==0 else MuralConstants.ENDTIME

    try:
        handle[MuralConstants.CREATERULE][t][0].click()
        setCalendar(timeObj.year,timeObj.month, timeObj.day, timeObj.hour, timeObj.min, instance, setup,MuralConstants.CREATERULEPOPUP)
        instance.reportspopup.clickButton("Apply", getHandle(setup, MuralConstants.CREATERULEPOPUP, Constants.ALLBUTTONS))
        dateSelected =  instance.dropdown.getValue_input(getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS),startEnd+1)
        logger.info("Date Selected %s for %s",str(dateSelected),str(t))
        return dateSelected
    except Exception as e:
        logger.error("Exception found while Selecting date %s for %s = %s",str(timeObj),str(t),str(e))
        return e

def setFilters(setup,valueArray,selectionByIndex=True):
    handles = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)

    filterDimension = setDrop(valueArray[0],len(handles[Constants.ALLSELECTS]["select"])-2,handles,selectionByIndex)
    filterValue = setDrop(valueArray[1],len(handles)-1,handles,selectionByIndex)
    return str(filterDimension)+":"+str(filterValue)
    return [filterDimension,filterValue]

def clickButton(setup,buttonName,input=False):
    instance = DropdownComponentClass()
    buttonHandle = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLBUTTONS)
    if input:
        return instance.clickInputButton(buttonName,buttonHandle)
    else:
        return instance.clickButton(buttonName,buttonHandle)

def doSearchAndValidateAlerts(setup):
    screenInstance = AlertsComponentClass()
    searchedtext = "Nokia"
    textEntered = screenInstance.search.sendkeys_input(searchedtext,getHandle(setup,MuralConstants.ALERTSCREEN,"search"),0,"search","searchInput")
    checkEqualAssert(searchedtext,textEntered,"","","Verify Search Text Entered")
    # screenInstance.search.setSearchText(getHandle(setup,MuralConstants.ALERTSCREEN,"search"),searchedtext)
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    for i in range(len(alertlist)):
        if searchedtext in alertlist[i]['header']:
            logger.info("Searched Text '%s' present in alert list '%s' ",searchedtext, alertlist[i]['header'])
        else:
            logger.info("Searched Text '%s' NOT present in alert list '%s' ",searchedtext, alertlist[i]['header'])
        checkEqualAssert(True,searchedtext in alertlist[i]['header'],"","","Searched Text '"+searchedtext+"' present in alert list = " + alertlist[i]['header'])
    t = screenInstance.search.sendkeys_input("",getHandle(setup,MuralConstants.ALERTSCREEN,"search"),0,"search","searchInput")
    # checkEqualAssert("",t,"","","Check Search Field Cleared")

def doCalendarSearchOnAlerts(setup):
    screenInstance = AlertsComponentClass()
    calHandler = getHandle(setup,MuralConstants.ALERTSCREEN,"search")
    logger.info("Launching Calendar from Search Panel")
    calHandler['search']['datepicker'][0].click()
    logger.info("Calendar picker is clicked")
    stObj = Time(2015,11,19,00,00)
    stEpoch = getepoch(stObj.datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")
    instance = GenerateReportsPopClass(setup.d)
    setCalendar(stObj.year,stObj.month, stObj.day, stObj.hour, stObj.min, instance, setup,MuralConstants.CREATERULEPOPUP)
    etObj = Time(2015,11,27,00,00)
    etEpoch = getepoch(etObj.datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")
    setCalendar(etObj.year,etObj.month, etObj.day, etObj.hour, etObj.min, instance, setup,MuralConstants.CREATERULEPOPUP,"rightcalendar")
    # Closing Calendar Pop Up
    instance.reportspopup.clickButton("Apply", getHandle(setup, MuralConstants.CREATERULEPOPUP, Constants.ALLBUTTONS))

    logger.info("Calendar Selection done at Search Panel = StartTime : %s and EndTimer : %s ",stObj.datestring,etObj.datestring)

    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")

    for i in range(len(alertlist)):
        actualStartTime,actualEndTime = parseTimeRange(alertlist[i]['duration'],MuralConstants.TIMEZONEOFFSET,"%d %m %Y %H:%M","-")
        # if (actualStartTime<=etEpoch and actualStartTime>=stEpoch) or (actualEndTime<=etEpoch and actualEndTime>=stEpoch):
        checkEqualAssert(True,(actualStartTime<=etEpoch and actualStartTime>=stEpoch) or (actualEndTime<=etEpoch and actualEndTime>=stEpoch),"","",
                         "Check for alert '%s' and duration = '%s' falling in filtered timerange (%s,%s) ",alertlist[i]['header'],alertlist[i]['duration'],stObj.datestring,etObj.datestring)

def acknowledgeAlert(setup,index):
    alertbodylinks = setup.cM.getNodeElements("alertbodylinks","link")
    screenInstance = AlertsComponentClass()
    screenInstance.selectAlert(index,getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"))
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    selectedAlertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","selected")

    # assuming selection is single
    selectedAlert=selectedAlertlist[0]

    if selectedAlert['state']:
        logger.debug("Alert is already acknowledged = %s",str(selectedAlert))
    else:
        logger.debug("Alert will be acknowledged = %s",str(selectedAlert))
        alertFullBody = screenInstance.getAlertFullBody(getHandle(setup,MuralConstants.ALERTSCREEN,"alertinfo"))
        logger.info("Got Acknowledge Status %s from Alert's Full Body = %s",str(alertFullBody['state']),str(alertFullBody))
        checkEqualAssert(selectedAlert['setup'],alertFullBody['state'],"","","Check for Uniform Handled Alert Status")

        screenInstance.dropdown.clickSpanWithTitle(alertbodylinks['acknowledge']['locatorText'],getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
        logger.info("Link %s is clicked",alertbodylinks['acknowledge']['locatorText'])

        updated_alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","selected")[0]
        updated_alertFullBody = screenInstance.getAlertFullBody(getHandle(setup,MuralConstants.ALERTSCREEN,"alertinfo"))
        logger.info("Got Acknowledge Status %s from Alert's Full Body = %s",str(updated_alertFullBody['state']),str(updated_alertFullBody))

        checkEqualAssert(True,updated_alertlist['state'],"","","Check for Alert status Handled or not in AlertList")
        checkEqualAssert(True,updated_alertFullBody['state'],"","","Check for Alert status Handled or not in AlertFullBody")

def deleteAllAlert(setup,index):
    alertbodylinks = setup.cM.getNodeElements("alertbodylinks","link")
    screenInstance = AlertsComponentClass()
    screenInstance.selectAlert(index,getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"))
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    selectedAlertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","selected")

    # assuming selection is single
    selectedAlert=selectedAlertlist[0]

    alertFullBody = screenInstance.getAlertFullBody(getHandle(setup,MuralConstants.ALERTSCREEN,"alertinfo"))
    screenInstance.dropdown.clickSpanWithTitle(alertbodylinks['deleteall']['locatorText'],getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))

    gHandle = getHandle(setup,MuralConstants.ALERTSCREEN,"alert")
    logger.debug("Confirming Delete from Pop up")
    try:
        gHandle['alert']['ok'][0].click()
        try:
            gHandle['alert']['ok'][0].click()
        except:
            pass
    except Exception as e:
        logger.error("Exception found while Deleting All Alerts %s with Rule %s  : %s",str(selectedAlert),alertFullBody['ruleName'],e)
        return e


    for el in alertlist:
        checkEqualAssert(True,alertFullBody['ruleName'] != el['ruleName'],"","","Check for each alert : "+str(el)+" from list for rule "+alertFullBody['ruleName'] + " deleted")

def checkAlertsCount(setup):
    screenInstance = AlertsComponentClass()
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    count,calCount = screenInstance.getTotalAlerts(alertlist,getHandle(setup,MuralConstants.ALERTSCREEN,"counter"))
    checkEqualDict(count,calCount,"","","Checking Counts on AlertsPage")

def editAlert(setup,h,index):
    screenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,MuralConstants.ALERTSCREEN,"table")
    tableData = screenInstance.table.getTableData1(tableHandle)

    # reportId = screenInstance.table.getColumnValueMap(tableData,index)
    logger.info("Going to Edit Alert = %s",tableData['rows'][index])
    try:
        screenInstance.dropdown.customClick(tableHandle['table']['download'][index])
        try:
            screenInstance.dropdown.customClick(getHandle(setup,MuralConstants.REPORTSCREEN,"table")['table']['edit'][index])
        except:
            pass
        logger.info("Editing Alert = %s",tableData['rows'][index])

        # checkEqualAssert(True,True,"","","Check for Download Report"+str(reportId))
        return True
    except Exception as e:
        # logger.error("Exception found while Downloading ReportId : %s",reportId)
        # checkEqualAssert(True,e,"","","Check for Download Report"+str(reportId))
        return e


def launchAlertWizard(setup,index):
    popInstance = GenerateReportsPopClass(setup.d)
    popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
    popInstance.switcher.switchTo(index,getHandle(setup,MuralConstants.ALERTSCREEN,"settings"),"settings")
    popInstance.dropdown.customClick(getHandle(setup,MuralConstants.ALERTSCREEN,"settings")['settings']['createrule'])
    return popInstance


def validateKPIAlertWizard(setup, request = {}):
    response = {}

    # mandatory conditions
    flag_rule = False
    flag_Gateway = False
    flag_Schema = False
    flag_KPI = False
    flag_Index = False
    flag_Gran = False
    flag_Threshold = False

    # bool = getBool
    max_character_length = 64

    # creating a random number
    rndmNum = random.randint(0,999999)
    popInstance = launchAlertWizard(setup,1)

    # Set each dropdown
    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
    request['gateway'] = setDrop("Mumbai",0, allselects)
    flag_Gateway = False if "Exception" in  request['gateway'] else True
    request['schema'] = setDrop("apn",1, allselects)
    flag_Schema = False if "Exception" in  request['schema'] else True
    request['kpi'] = setDrop("Packet Drop",2, allselects)
    flag_KPI = False if "Exception" in  request['kpi'] else True

    request['index'] = setDropRandomly(3, allselects)
    flag_Index = False if "Exception" in  request['index'] else True
    request['gran'] = setDropRandomly(4, allselects)
    flag_Gran = False if "Exception" in  request['gran'] else True

    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    # check for all the options in RuleName
    rulenames = setup.cM.getNodeElements("rulenames","rulename")
    for k,rulename in rulenames.iteritems():
        checkEqualAssert(rulename['expected'],setName(rulename['text'],getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS)),
                         "","","Verified for rule Name :"+rulename['text'])

        dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    thresholds = setup.cM.getNodeElements("kpithresholds","threshold")
    for severity in range(4):
        for k,threshold in thresholds.iteritems():
            request['conditions'] = []
            request['conditions'].append(setKPICondition(severity,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5,enableCondition=False,thresholdValue=threshold['text']))
            # number_value=re.findall(r'\d+',request['conditions'][0])[0]
            number_value = request['conditions'][0].split(re.findall('[=<>]+',request['conditions'][0])[0])[1]
            checkEqualAssert(threshold['expected'],str(number_value),
                         "","","Verified for Threshold Values :"+threshold['text'])
        dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    request['conditions'] = []
    request['conditions'].append(setKPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5,enableCondition=True,thresholdValue=""))
    flag_Threshold = False if re.findall(r'\d+', request['conditions'][0]) == [] else True
    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    num_value = popInstance.sendkeys_input("123", getHandle(setup, MuralConstants.CREATERULEPOPUP, "allinputs"),1, "allinputs")
    flag_Threshold = False if not num_value else True

    request['ruleName'] = setName("", getHandle(setup, MuralConstants.CREATERULEPOPUP, Constants.ALLINPUTS))
    flag_rule = False if request['ruleName'] == "" else True

    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule, request,popInstance, setup)

    rulename = "automationrule"+str(rndmNum)
    request['ruleName'] = setName(rulename,getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS))
    flag_rule = False if request['ruleName'] == "" else True

    dumpResultForButton(
        flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule, request,
        popInstance, setup)

    request['conditions'] = []
    request['conditions'].append(setKPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    if request['conditions'][0] != "-":
        flag_Threshold = True
    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    request['conditions'].append(setKPICondition(1,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    if request['conditions'][1] != "-":
        flag_Threshold = True

    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)
    request['conditions'].append(setKPICondition(2,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    if request['conditions'][2] != "-":
        flag_Threshold = True
    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)
    request['conditions'].append(setKPICondition(3,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    if request['conditions'][3] != "-":
        flag_Threshold = True
    dumpResultForButton(flag_rule and flag_Threshold and flag_Gran and flag_Index and flag_KPI and flag_Schema and flag_rule,request,popInstance,setup)

    # request['status'] = "Active"

    # clickButton(setup,"Create")

def dumpResultForButton(condition,request,popInstance,setup):
    checkEqualAssert(condition,popInstance.reportspopup.isButtonEnabled("Create",getHandle(setup, MuralConstants.CREATERULEPOPUP, "allbuttons")),
                     "","","Checking State of Create/Submit Button for Fields entered : "+str(request))

def getBool(*args):
    bool = False
    for arg in args:
        bool = bool and arg
    return bool

def validateDPIAlertWizard(setup,request={}):
    # creating a random number
    rndmNum = random.randint(0,999999)

    popInstance = launchAlertWizard(setup,0)

    # mandatory conditions
    flag_rule = False
    flag_measure = False
    flag_type = False
    flag_gran = False
    flag_st = False
    flag_et = False
    flag_threshold = False

    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
    request['measure'] = setDrop(request['measure']['locatorText'],0,allselects)
    request['type'] = setDrop(request['type'],1,allselects)
    request['gran'] = setDrop(request['gran'],2,allselects)
    flag_measure = False if "Exception" in  request['measure'] else True
    flag_type = False if "Exception" in  request['type'] else True
    flag_gran = False if "Exception" in  request['gran'] else True

    # check for all the options in RuleName
    rulenames = setup.cM.getNodeElements("rulenames","rulename")
    for k,rulename in rulenames.iteritems():
        checkEqualAssert(rulename['expected'],setName(rulename['text'],getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS)),
                         "","","Verified for rule Name :"+rulename['text'])
        dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    thresholds = setup.cM.getNodeElements("dpithresholds","threshold")
    for severity in range(4):
        for k,threshold in thresholds.iteritems():
            request['conditions'] = []
            request['conditions'].append(setDPICondition(severity,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3,enableCondition=False,thresholdValue=threshold['text']))
            number_value=re.findall(r'\d+',request['conditions'][0])[0]
            # number_value = request['conditions'][0].split(re.findall('[=<>]+',request['conditions'][0])[0])[1]
            checkEqualAssert(threshold['expected'],str(number_value),
                         "","","Verified for Threshold Values :"+threshold['text'])
        dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    request['conditions'] = []
    request['conditions'].append(setDPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3,enableCondition=True,thresholdValue=""))
    flag_threshold = False if re.findall(r'\d+', request['conditions'][0]) == [] else True
    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    num_value = popInstance.sendkeys_input("123", getHandle(setup, MuralConstants.CREATERULEPOPUP, "allinputs"),1, "allinputs")
    flag_threshold = False if not num_value else True

    request['conditions'] = []
    request['conditions'].append(setDPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3,enableCondition=True,thresholdValue="0"))
    flag_threshold = False if re.findall(r'\d+', request['conditions'][0]) == [] else True
    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    num_value = popInstance.sendkeys_input("123", getHandle(setup, MuralConstants.CREATERULEPOPUP, "allinputs"),1, "allinputs")
    flag_threshold = False if not num_value else True



    request['ruleName'] = setName("", getHandle(setup, MuralConstants.CREATERULEPOPUP, Constants.ALLINPUTS))
    flag_rule = False if request['ruleName'] == "" else True

    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    rulename = "automationrule"+str(rndmNum)
    request['ruleName'] = setName(rulename,getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLINPUTS))
    flag_rule = False if request['ruleName'] == "" else True

    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    request['conditions'] = []
    request['conditions'].append(setDPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3))
    if request['conditions'][0] != "-":
        flag_threshold = True
    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    request['conditions'].append(setDPICondition(1,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3))
    if request['conditions'][1] != "-":
        flag_threshold = True

    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)
    request['conditions'].append(setDPICondition(2,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3))
    if request['conditions'][2] != "-":
        flag_threshold = True
    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)
    request['conditions'].append(setDPICondition(3,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,3))
    if request['conditions'][3] != "-":
        flag_threshold = True
    dumpResultForButton(flag_rule and flag_measure and flag_type and flag_gran and flag_st and flag_et and flag_threshold,request,popInstance,setup)

    startEndTimeValidations(setup,request)

def startEndTimeValidations(setup,request = {}):

    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
    request['measure'] = setDrop(request['measure']['locatorText'],0,allselects)
    request['type'] = setDrop(request['type'],1,allselects)
    request['gran'] = setDrop(request['gran'],2,allselects)
    flag_measure = False if "Exception" in  request['measure'] else True
    flag_type = False if "Exception" in  request['type'] else True
    flag_gran = False if "Exception" in  request['gran'] else True

    starttime = setup.cM.getNodeElements("dpiWizardtimerange","startime")
    for k,starttime in starttime.iteritems():
        st = Time(starttime['year'],starttime['month'],starttime['day'],starttime['hour'],starttime['minute'])

    starttimeEpoch = getepoch(st.datestring,Constants.TIMEZONEOFFSET,"%Y-%m-%d %H:%M")

    request[MuralConstants.STARTTIME]=setTime(setup,0,st)

    request['time'][1]= getEndtime(setup, request['type'], request['gran'], starttimeEpoch,Constants.TIMEZONEOFFSET)

    request[MuralConstants.ENDTIME] = setTime(setup,1,request['time'][1])












