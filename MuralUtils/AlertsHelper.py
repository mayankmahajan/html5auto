#!/usr/bin/env python
##############################################################
'''
Called Directly from TestCase
'''
from classes.Objects import CreateAlert

__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################


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
    request["range"] = str(getDateString(starttimeEpoch,Constants.TIMEZONEOFFSET,"%a %b %d %Y")) +" to "+ str(getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%a %b %d %Y"))


    response['filters'] = ""
    for i in range(len(request['filters'])):
        response['filters'] = response['filters']+setFilters(setup,request['filters'][i])+','
        if i < len(request['filters'])-1:
            clickButton(setup,"add",True)

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
    #
    allselects = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)

    request['gateway'] = setDropRandomly(0, allselects)
    request['schema'] = setDropRandomly(1, allselects)
    request['kpi'] = setDropRandomly(2, allselects)
    request['index'] = setDropRandomly(3, allselects)
    request['gran'] = setDropRandomly(4, allselects)

    request['conditions'] = []
    request['conditions'].append(setKPICondition(0,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(1,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(2,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))
    request['conditions'].append(setKPICondition(3,getHandle(setup,MuralConstants.CREATERULEPOPUP,"allcheckboxes"),setup,5))

    clickButton(setup,"Create")

    checkKPIAlertTableForCreatedRecord(setup,request)

def checkDPIAlerts(setup):
    popInstance = GenerateReportsPopClass(setup.d)
    # Launching Settings Page
    # popInstance.dropdown.clickSpanWithTitle("Settings",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
    alertRuleMap = {}
    # alertRuleMap= getTableDataMap(setup, MuralConstants.ALERTSCREEN)
    popInstance.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS))
    screenInstance = AlertsComponentClass()
    alertlist = screenInstance.getAlertList(getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"),"alertlist","list")
    checkAlertsPresent(setup,alertRuleMap,alertlist)

def checkAlertsPresent(setup,alertRuleMap,alertlist):
    for i in range(len(alertlist)):
        screenInstance = AlertsComponentClass()
        screenInstance.selectAlert(i,getHandle(setup,MuralConstants.ALERTSCREEN,"alertlist"))
        screenInstance.getAlertFullBody(getHandle(setup,MuralConstants.ALERTSCREEN,"alertinfo"))






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
            return int(starttimeEpoch) + (3+random.randint(1,3))*86400*30
        else:
            return int(starttimeEpoch) + (21+random.randint(1,3))*86400
    return int(starttimeEpoch) + int(ran)*2592000

def createTimeFromEpoch(epoch,timezone):
    pattern = "%Y-%m-%d-%H-%M"
    parts=getDateString(epoch,timezone,pattern).split("-")
    return Time(parts[0],parts[1],parts[2],parts[3])

     # = getDateString(endtimeEpoch,Constants.TIMEZONEOFFSET,"%Y-%m-%d-%H-%M")

def checkDPIAlertTableForCreatedRecord(setup,request,index=0):

    reportScreenInstance = ReportsModuleClass(setup.d)

    # saving the table data as keys
    tableMap = getTableDataMap(setup,MuralConstants.ALERTSCREEN)

    # reportScreenInstance.switcher.switchTo(1,getHandle(setup,MuralConstants.REPORTSCREEN,"createdialog"))


    # r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Name")
    # r = reportScreenInstance.table.sortTable1(getHandle(setup,MuralConstants.REPORTSCREEN,"table"),"Id")

    data = reportScreenInstance.table.getTableData1(getHandle(setup,MuralConstants.ALERTSCREEN,"table"),"table")

    actual ={}
    row = tableMap['rows'][request['ruleName']]
    print row

    actual['ruleName'] = row[0]
    actual['gran'] = row[1]
    actual['filters'] = row[2]
    actual['measure'] = row[3]
    actual['conditions'] = [row[4],row[5],row[6]]
    actual['range'] = row[7]
    actual['status'] = row[8]


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
    reportScreenInstance = ReportsModuleClass(setup.d)
    # saving the table data as keys
    tableMap = getTableDataMap(setup,MuralConstants.ALERTSCREEN)
    data = reportScreenInstance.table.getTableData1(getHandle(setup,MuralConstants.ALERTSCREEN,"table"),"table")

    actual ={}
    row = tableMap['rows'][request['ruleName']]
    print row
    actual['ruleName'] = row[0]
    actual['schema'] = row[1]
    actual['kpi'] = row[2]
    actual['index'] = row[3]
    actual['conditions'] = [row[4],row[5],row[6],row[7]]
    actual['status'] = row[8]

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

def setDPICondition(priorty, cond, handle, setup,firstDrop=3):

    # operator=re.findall('[=<>]+',cond)
    # number_value=re.findall(r'\d+',cond)
    # unitSystem=re.findall('[a-zA-Z]+',cond)
    #
    # operator=cond[0]
    # number_value=cond[1]
    # unitSystem=cond[2]

    operator=re.findall('[=<>]+',cond)[0]
    number_value=re.findall(r'\d+',cond)[0]

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
            return str(op).strip()+str(num_value).strip()
        else:
            logger.info("Selecting unitsystem %s for operator %s and Priority %s",str(unitSystem),str(operator),str(priorty))
            unit=instance.doSelectionOnVisibleDropDown(handle,unitSystem,index+1)
            logger.info("Unitsystem %s is set for operator %s and Priority %s",str(unitSystem),str(operator),str(priorty))
            return str(op).strip()+str(num_value).strip()+str(unit).strip()


    except Exception as e:
        logger.error("Exception found while setting condition at CreateRule for DPI [Priority: %s, Operator: %s, Value: %s, Unit: %s  =  %s",
                     str(priorty),str(operator),str(number_value),str(unitSystem), str(e) )
        return e

def setKPICondition(priorty, handle, setup,firstDrop=3):
    if priorty==0:
        index = firstDrop
    elif priorty==1:
        index = firstDrop+1
    elif priorty==2:
        index = firstDrop+2
    elif priorty==3:
        index = firstDrop+3

    try:
        instance = DropdownComponentClass()
        logger.info("Enabling Priority %s",str(priorty))
        instance.clickCheckBox(handle,priorty)
        logger.info("Priority %s is selected",str(priorty))
        handle = getHandle(setup,MuralConstants.CREATERULEPOPUP,Constants.ALLSELECTS)
        op=instance.doRandomSelectionOnVisibleDropDown(handle,index)
        logger.info("Operator %s for Priority %s is selected",str(op),str(priorty))
        num_value = instance.sendkeys_input(random.randint(0,100), getHandle(setup,MuralConstants.CREATERULEPOPUP,"allinputs"),priorty+1,"allinputs")
        logger.info("Value %s set for operator %s and Priority %s",str(num_value),str(op),str(priorty))

        if random.choice([True, False]):
            return str(op).strip()+str(num_value).strip()
        else:
            if random.choice([True, False]):
                return str(op).strip()+str(num_value).strip()
            else:
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

