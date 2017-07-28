from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from Utils.SetUp import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import random

def isSnappingFromUI(setup,page=Constants.CALENDERPOPUP,rightSpanParent='rightSpanInfo',leftSpanParent='leftSpanInfo',child='span'):
    rightSpanHandle=getHandle(setup,page,rightSpanParent)
    leftSpanHandle=getHandle(setup,page,leftSpanParent)
    SpanList=[]
    rightSpanValue=''
    leftSpanValue=''

    if len(leftSpanHandle[leftSpanParent][child]) > 0 or len(rightSpanHandle[rightSpanParent][child])>0:
        if len(leftSpanHandle[leftSpanParent][child]) > 0:
            leftSpanValue = str(leftSpanHandle[leftSpanParent][child][0].text)

        if len(rightSpanHandle[rightSpanParent][child])>0:
            rightSpanValue=str(rightSpanHandle[rightSpanParent][child][0].text)

        SpanList.append(leftSpanValue.lstrip('(snaps to').rstrip(')'))
        SpanList.append(rightSpanValue.lstrip('(snaps to').rstrip(')'))

        return True,SpanList
    else:
        return False,['','']

def launchCalendar(setup,Page,parent='ktrs',child='datepicker',index=0):
    calHandler = getHandle(setup, Page,parent)
    logger.info("Launching Calendar: ")
    calHandler[parent][child][index].click()
    logger.info("Calendar picker is clicked")

def getDefaultRightCalendarValue(setup,parent='allspans',child='span',index=0):
    defaultValueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, parent)[parent][child][index].text).strip()
    if len(defaultValueFromCalender.split('to'))>1:
        if len(defaultValueFromCalender.split('to')[1].strip().split(' '))==3:
            endDateString=defaultValueFromCalender.split('to')[1].strip()+' 00:00'
            return getepoch(endDateString, tPattern='%d %b %Y %H:%M')+86400
        else:
            endDateString=defaultValueFromCalender.split('to')[1]
            return getepoch(endDateString, tPattern='%d %b %Y %H:%M')
    elif len(defaultValueFromCalender.split('to'))==1:
        endDateString = defaultValueFromCalender+' 00:00'
        return getepoch(endDateString, tPattern='%d %b %Y %H:%M')+86400

def isSnapping(epochOfFirstSelection,epochOfLastSelection,pointDict,snap_Side='right'):
    possiblePointForFirstSelection=[]
    for key in availablepoint:
        if checkInRange(epochOfFirstSelection,pointDict,key):
            possiblePointForFirstSelection.append(int(key))

    grainForFirstSelection=str(min(possiblePointForFirstSelection))

    possiblePointForLastSelection = []
    for key in availablepoint:
        if checkInRange(epochOfLastSelection,pointDict,key):
            possiblePointForLastSelection.append(int(key))

    grainForLastSelection = str(min(possiblePointForLastSelection))

    if grainForLastSelection=='86400' or grainForLastSelection=='2592000':
        if grainForFirstSelection == '3600':
            if (epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400==0:
                grainForFirstSelection='86400'

    if grainForFirstSelection==grainForLastSelection:
        return False,''

    elif grainForLastSelection=='86400':
        if snap_Side=='right':

            if checkInRange(epochOfFirstSelection+(86400-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400),availablepointEpoch,grainForLastSelection):
                return True,epochOfFirstSelection+(86400-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400)

            elif checkInRange(epochOfFirstSelection-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400,availablepointEpoch,grainForLastSelection):
                return True,epochOfFirstSelection-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400

            else:
                return True,availablepointEpoch[grainForLastSelection]['endtime']

        elif snap_Side=='left':
            if checkInRange(epochOfFirstSelection-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400,availablepointEpoch,grainForLastSelection):
                return True,epochOfFirstSelection-(epochOfFirstSelection+Constants.TIMEZONEOFFSET*3600)%86400
            else:
                return True,availablepointEpoch[grainForLastSelection]['starttime']


    elif grainForLastSelection=='3600':
        if snap_Side=='right':
            if checkInRange(epochOfFirstSelection,availablepointEpoch,grainForLastSelection):
                return True,epochOfFirstSelection
            else:
                return True,availablepointEpoch[grainForLastSelection]['endtime']

        elif snap_Side=='left':
            if checkInRange(epochOfFirstSelection,availablepointEpoch,grainForLastSelection):
                return True,epochOfFirstSelection
            else:
                return True,availablepointEpoch[grainForLastSelection]['starttime']

    elif grainForLastSelection=='2592000':
        if snap_Side=='right':
            if checkInRange(epochOfFirstSelection,availablepointEpoch,grainForLastSelection):
                dateString = getDateString(epochOfLastSelection, tPattern='%Y %m %d %H %M')
                import calendar
                monthEndDate=calendar.monthrange(int(dateString[0]),int(dateString[1]))[1]
                return True,getepoch(dateString[0]+' '+dateString[1]+' '+str(monthEndDate)+' 00:00',tPattern='%Y %m %d %H:%M')+86400
            else:
                return True,availablepointEpoch[grainForLastSelection]['endtime']

        elif snap_Side=='left':
            if checkInRange(epochOfFirstSelection,availablepointEpoch,grainForLastSelection):
                dateString = getDateString(epochOfLastSelection, tPattern='%Y %m %d %H %M')
                import calendar
                monthEndDate=calendar.monthrange(int(dateString[0]),int(dateString[1]))[1]
                return True,getepoch(dateString[0]+' '+dateString[1]+' '+str(monthEndDate)+' 00:00',tPattern='%Y %m %d %H:%M')
            else:
                return True,availablepointEpoch[grainForLastSelection]['starttime']

def selfSnapping(epochOfLastSelection,pointDict,snap_Side='left'):
    possiblePointForLastSelection = []
    for key in availablepoint:
        if checkInRange(epochOfLastSelection,pointDict,key):
            possiblePointForLastSelection.append(int(key))

    grainForLastSelection = str(min(possiblePointForLastSelection))

    if grainForLastSelection == '86400':
        if snap_Side == 'left':
            if checkInRange(epochOfLastSelection - (epochOfLastSelection + Constants.TIMEZONEOFFSET * 3600) % 86400,availablepointEpoch, grainForLastSelection):
                return True, epochOfLastSelection - (epochOfLastSelection + Constants.TIMEZONEOFFSET * 3600) % 86400
            else:
                return True, availablepointEpoch[grainForLastSelection]['startime']

    if grainForLastSelection=='2592000':
        if snap_Side=='left':
            if checkInRange(epochOfLastSelection,availablepointEpoch,grainForLastSelection):
                dateString=getDateString(epochOfLastSelection,tPattern='%Y %B %d %H %M')
                return True,(epochOfLastSelection-(int(dateString[3])+Constants.TIMEZONEOFFSET)*3600)
            else:
                return True,availablepointEpoch[grainForLastSelection]['startime']


    if grainForLastSelection=='3600':
        if snap_Side=='right':
            if checkInRange(epochOfLastSelection,availablepointEpoch,grainForLastSelection):
                return True,epochOfLastSelection
            else:
                return True,availablepointEpoch[grainForLastSelection]['startime']
    return False,''


def checkInRange(value,availablepointEpoch,key):
    if availablepointEpoch[key]['starttime'] <= value and value <=availablepointEpoch[key]['endtime']:
        return True
    else:
        return False


def time_format(starttime,endtime):
    if starttime.split(" ")[3].split(":")[0]=='00' and endtime.split(" ")[3].split(":")[0]=='00':
        endtimeEpoch=getepoch(endtime)
        endtimeEpoch=endtimeEpoch-3600
        endtime=getDateString(endtimeEpoch)
        return starttime.split(" ")[0] + " " + starttime.split(" ")[1] + " " + starttime.split(" ")[2] + " to " + endtime.split(" ")[0] + " " + endtime.split(" ")[1] + " " + endtime.split(" ")[2]
    elif endtime.split(" ")[3].split(":")[0]=='00':
        endtimeEpoch = getepoch(endtime)
        endtimeEpoch = endtimeEpoch - 3600
        endtime = getDateString(endtimeEpoch)
        return starttime + " to " + endtime.split(" ")[0] + " " + endtime.split(" ")[1] + " " + endtime.split(" ")[2]+" 24:00"
    else:
        return starttime+" to "+endtime


def formattedEndTime(endtime):
    if endtime.split(" ")[3].split(":")[0]=='00':
        endtimeEpoch = getepoch(endtime)
        endtimeEpoch = endtimeEpoch - 3600
        endtime = getDateString(endtimeEpoch)
        return endtime.split(" ")[0] + " " + endtime.split(" ")[1] + " " + endtime.split(" ")[2]+" 24:00"
    else:
        return endtime

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    availablepoint= {}
    availablepointEpoch={}
    availablepoint=setup.cM.getNodeElements("availabletimerangepoint","point")

    launchCalendar(setup,MRXConstants.UDPPOPUP)

    hourlyStartEpoch=0
    hourlyEndEpoch=0
    dailyStartEpoch=0
    dailyEndEpoch=0
    monthlyStartEpoch=0
    monthlyEndEpoch=0

    if '3600' in availablepoint.keys():
        availablepointEpoch['3600']={}
        hourlyStartEpoch =getepoch(availablepoint['3600']['starttime'])
        hourlyEndEpoch =getepoch(availablepoint['3600']['endtime'])
        availablepointEpoch['3600']['starttime']=hourlyStartEpoch
        availablepointEpoch['3600']['endtime']=hourlyEndEpoch

    if '86400' in availablepoint.keys():
        availablepointEpoch['86400']={}
        dailyStartEpoch =getepoch((availablepoint['86400']['starttime']))
        dailyEndEpoch =getepoch((availablepoint['86400']['endtime']))
        availablepointEpoch['86400']['starttime']=dailyStartEpoch
        availablepointEpoch['86400']['endtime']=dailyEndEpoch


    if '2592000' in availablepoint.keys():
        availablepointEpoch['2592000'] = {}
        monthlyStartEpoch =getepoch((availablepoint['2592000']['starttime']))
        monthlyEndEpoch =getepoch((availablepoint['2592000']['endtime']))
        availablepointEpoch['2592000']['starttime'] = monthlyStartEpoch
        availablepointEpoch['2592000']['endtime'] = monthlyEndEpoch


    ####################################################################################################################

    if '3600' in availablepoint.keys():

        # Set Start Point (Hourly)

        dateStringStart = getDateString(hourlyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        #1

        dateStringEnd = getDateString(hourlyEndEpoch, tPattern='%Y %B %d %H %M').split(' ')
        if dateStringEnd[3]=='00':
            dateStringEnd=getDateString(hourlyEndEpoch-3600, tPattern='%Y %B %d %H %M').split(' ')
            dateStringEnd[3]='24'
        setCalendar(dateStringEnd[0], dateStringEnd[1], dateStringEnd[2], dateStringEnd[3], dateStringEnd[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue=isSnapping(hourlyStartEpoch,hourlyEndEpoch,availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch),getDateString(hourlyEndEpoch))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #2

        dateString = getDateString(hourlyEndEpoch-3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(hourlyStartEpoch, hourlyEndEpoch-3600, availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch),getDateString(hourlyEndEpoch-3600))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #3

        n=random.randrange((hourlyEndEpoch-hourlyStartEpoch)/3600)
        dateString = getDateString(hourlyStartEpoch+n*3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(hourlyStartEpoch, hourlyStartEpoch+n*3600, availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch),getDateString(hourlyStartEpoch+n*3600))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

    # Set End Point (Hourly)

        dateStringEnd = getDateString(hourlyEndEpoch, tPattern='%Y %B %d %H %M').split(' ')
        if dateStringEnd[3] == '00':
            dateStringEnd = getDateString(hourlyEndEpoch - 3600, tPattern='%Y %B %d %H %M').split(' ')
            dateStringEnd[3] = '24'
        setCalendar(dateStringEnd[0], dateStringEnd[1], dateStringEnd[2], dateStringEnd[3], dateStringEnd[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="rightcalendar")

        # 1

        dateStringStart = getDateString(hourlyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue=isSnapping(hourlyEndEpoch,hourlyStartEpoch,availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch),getDateString(hourlyEndEpoch))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #2

        dateString = getDateString(hourlyStartEpoch+3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(hourlyEndEpoch, hourlyStartEpoch+3600, availablepointEpoch)

        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch+3600),getDateString(hourlyEndEpoch))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #3

        n=random.randrange((hourlyEndEpoch-hourlyStartEpoch)/3600)
        dateString = getDateString(hourlyStartEpoch+n*3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(hourlyEndEpoch, hourlyStartEpoch+n*3600, availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        expectedText=time_format(getDateString(hourlyStartEpoch+n*3600),getDateString(hourlyEndEpoch))
        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #4

        dateString = getDateString(hourlyStartEpoch-3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(hourlyEndEpoch, hourlyStartEpoch-3600, availablepointEpoch,snap_Side='right')
        selfSnapFlag,selfSnapValue=selfSnapping(hourlyStartEpoch-3600,availablepointEpoch,snap_Side='left')

        checkEqualAssert(value[0],getDateString(selfSnapValue),message='Verify left Snapped Value')
        checkEqualAssert(value[1],formattedEndTime(getDateString(snapValue)),message='Verify Right Snapped Value')
        checkEqualAssert(flagBE,flag,message='Verify Snapping')


        if flagBE and selfSnapFlag:
           expectedText=time_format(getDateString(selfSnapValue),getDateString(snapValue))
        elif flagBE:
            expectedText = time_format(getDateString(hourlyStartEpoch-3600), getDateString(snapValue))
        else:
            expectedText = time_format(getDateString(hourlyStartEpoch - 3600), getDateString(hourlyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #5
        if '2592000' in availablepoint.keys():
            dateString = getDateString(monthlyStartEpoch + 3600, tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

            flag, value = isSnappingFromUI(setup)
            flagBE, snapValue = isSnapping(hourlyEndEpoch, monthlyStartEpoch + 3600, availablepointEpoch, snap_Side='right')
            selfSnapFlag, selfSnapValue = selfSnapping(monthlyStartEpoch + 3600, availablepointEpoch, snap_Side='left')

            checkEqualAssert(value[0], getDateString(selfSnapValue), message='Verify left Snapped Value')
            checkEqualAssert(value[1], formattedEndTime(getDateString(snapValue)), message='Verify Right Snapped Value')
            checkEqualAssert(flagBE, flag, message='Verify Snapping')

            if flagBE and selfSnapFlag:
                expectedText = time_format(getDateString(selfSnapValue), getDateString(snapValue))
            elif flagBE:
                expectedText = time_format(getDateString(monthlyStartEpoch + 3600), getDateString(snapValue))
            else:
                expectedText = time_format(getDateString(monthlyStartEpoch + 3600), getDateString(hourlyEndEpoch))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText, valueFromCalender, message='Verify TimeRange on Calendar')


    ####################################################################################################################

    if '86400' in availablepoint.keys():

    # Set Start Point (Hourly)

        dateStringStart = getDateString(dailyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        #1

        dateStringEnd = getDateString(dailyEndEpoch, tPattern='%Y %B %d %H %M').split(' ')
        if dateStringEnd[3]=='00':
            dateStringEnd=getDateString(dailyEndEpoch-3600, tPattern='%Y %B %d %H %M').split(' ')
            dateStringEnd[3]='24'
        setCalendar(dateStringEnd[0], dateStringEnd[1], dateStringEnd[2], dateStringEnd[3], dateStringEnd[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue=isSnapping(dailyStartEpoch,dailyEndEpoch,availablepointEpoch,snap_Side='left')

        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText=time_format(getDateString(snapValue),getDateString(dailyEndEpoch))
            checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(dailyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #2

        dateString = getDateString(dailyEndEpoch-86400, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(dailyStartEpoch, dailyEndEpoch-86400, availablepointEpoch,snap_Side='left')
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText = time_format(getDateString(snapValue), getDateString(dailyEndEpoch - 86400))
            checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(dailyEndEpoch - 86400))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #3

        n=random.randrange((dailyEndEpoch-dailyStartEpoch)/86400)
        dateString = getDateString(dailyStartEpoch+n*86400, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(dailyStartEpoch, dailyStartEpoch+n*86400, availablepointEpoch,snap_Side='left')
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText = time_format(getDateString(snapValue), getDateString(dailyStartEpoch + n * 86400))
            checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(dailyStartEpoch + n * 86400))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')


        #4
        dateString = getDateString(dailyEndEpoch+3600, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(dailyStartEpoch, dailyEndEpoch+3600, availablepointEpoch,snap_Side='left')
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText = time_format(getDateString(snapValue), getDateString(dailyEndEpoch+3600))
            checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(dailyEndEpoch+3600))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')


    # Set End Point (Hourly)

        dateStringEnd = getDateString(dailyEndEpoch, tPattern='%Y %B %d %H %M').split(' ')
        if dateStringEnd[3] == '00':
            dateStringEnd = getDateString(dailyEndEpoch - 3600, tPattern='%Y %B %d %H %M').split(' ')
            dateStringEnd[3] = '24'
        setCalendar(dateStringEnd[0], dateStringEnd[1], dateStringEnd[2], dateStringEnd[3], dateStringEnd[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="rightcalendar")

        # 1

        dateStringStart = getDateString(dailyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue=isSnapping(dailyEndEpoch,dailyStartEpoch,availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')
        if flagBE:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(snapValue))
            checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch), getDateString(dailyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #2

        dateString = getDateString(dailyStartEpoch+86400, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(dailyEndEpoch, dailyStartEpoch+86400, availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText = time_format(getDateString(dailyStartEpoch + 86400), getDateString(snapValue))
            checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch + 86400), getDateString(dailyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #3
        n = random.randrange((dailyEndEpoch - dailyStartEpoch) / 86400)
        dateString = getDateString(dailyStartEpoch + n * 86400, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue = isSnapping(dailyEndEpoch, dailyStartEpoch+n*86400, availablepointEpoch)
        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText = time_format(getDateString(dailyStartEpoch + n * 86400), getDateString(snapValue))
            checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(dailyStartEpoch + n * 86400), getDateString(dailyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')


        #4
        if '2592000' in availablepoint.keys():
            dateString = getDateString(monthlyStartEpoch+3600,tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="leftcalendar")

            flag,value = isSnappingFromUI(setup)
            flagBE,snapValue = isSnapping(dailyEndEpoch, monthlyStartEpoch+3600,availablepointEpoch,snap_Side='right')
            selfSnapFlag,selfSnapValue=selfSnapping(monthlyStartEpoch+3600,availablepointEpoch,snap_Side='left')

            checkEqualAssert(value[0],getDateString(selfSnapValue),message='Verify left Snapped Value')
            checkEqualAssert(value[1],formattedEndTime(getDateString(snapValue)),message='Verify Right Snapped Value')
            checkEqualAssert(flagBE,flag,message='Verify Snapping')


            if flagBE and selfSnapFlag:
               expectedText=time_format(getDateString(selfSnapValue),getDateString(snapValue))
            elif flagBE:
                expectedText = time_format(getDateString(monthlyStartEpoch+3600), getDateString(snapValue))
            else:
                expectedText = time_format(getDateString(monthlyStartEpoch+3600), getDateString(dailyEndEpoch))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')


    ####################################################################################################################

    if '2592000' in availablepoint.keys():

        # Set Start Point (Monthly)

        dateStringStart = getDateString(monthlyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
        setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

        #1

        dateStringEnd = getDateString(monthlyEndEpoch, tPattern='%Y %B %d %H %M').split(' ')
        if dateStringEnd[3]=='00':
            dateStringEnd=getDateString(monthlyEndEpoch-3600, tPattern='%Y %B %d %H %M').split(' ')
            dateStringEnd[3]='24'
        setCalendar(dateStringEnd[0], dateStringEnd[1], dateStringEnd[2], dateStringEnd[3], dateStringEnd[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

        flag,value = isSnappingFromUI(setup)
        flagBE,snapValue=isSnapping(monthlyStartEpoch,monthlyEndEpoch,availablepointEpoch,snap_Side='left')

        checkEqualAssert(flagBE,flag,message='Verify Snapping')

        if flagBE:
            expectedText=time_format(getDateString(snapValue),getDateString(monthlyEndEpoch))
            checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
        else:
            expectedText = time_format(getDateString(monthlyStartEpoch), getDateString(monthlyEndEpoch))

        valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
        checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

        #2

        if '86400' in availablepoint.keys():
            n = random.randrange((dailyEndEpoch - dailyStartEpoch) / 86400)
            dateString = getDateString(dailyStartEpoch + n * 86400, tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateString[0], dateString[1], dateString[2], dateString[3], dateString[4], udScreenInstance, setup,page=Constants.CALENDERPOPUP, parent="rightcalendar")

            flag,value = isSnappingFromUI(setup)
            flagBE,snapValue = isSnapping(monthlyStartEpoch, dailyStartEpoch + n * 86400, availablepointEpoch,snap_Side='left')
            checkEqualAssert(flagBE,flag,message='Verify Snapping')

            if flagBE:
                expectedText = time_format(getDateString(snapValue), getDateString(dailyStartEpoch + n * 86400))
                checkEqualAssert(getDateString(snapValue),value[0],message='Verify Snapped Value')
            else:
                expectedText = time_format(getDateString(monthlyStartEpoch), getDateString(dailyStartEpoch + n * 86400))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

    udScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))


    ##################################################### Default Scenario #############################################

    qs = ConfigManager().getNodeElements("wizardquicklinks1", "wizardquicklink")
    quicklink = ConfigManager().getAllNodeElements("wizardquicklinks1", "wizardquicklink")
    for e in quicklink:
        udScreenInstance.timeBar.setQuickLink(qs[e]['locatorText'], getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
        isError(setup)
        selectedQuicklink = udScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))

        if '3600' in availablepoint.keys():
            launchCalendar(setup, MRXConstants.UDPPOPUP)
            defaultRightValue=getDefaultRightCalendarValue(setup)
            dateStringStart = getDateString(hourlyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

            flag,value = isSnappingFromUI(setup)
            flagBE,snapValue=isSnapping(defaultRightValue,hourlyStartEpoch,availablepointEpoch)
            checkEqualAssert(flagBE,flag,selectedQuicklink,message='Verify Snapping')

            if flagBE:
                expectedText=time_format(getDateString(hourlyStartEpoch),getDateString(snapValue))
                checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],selectedQuicklink, message='Verify Snapped Value')
            else:
                expectedText = time_format(getDateString(hourlyStartEpoch), getDateString(defaultRightValue))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText,valueFromCalender,selectedQuicklink,message='Verify TimeRange on Calendar')

            udScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))


        if '86400' in availablepoint.keys():
            launchCalendar(setup, MRXConstants.UDPPOPUP)
            defaultRightValue=getDefaultRightCalendarValue(setup)
            dateStringStart = getDateString(dailyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

            flag,value = isSnappingFromUI(setup)
            flagBE,snapValue=isSnapping(defaultRightValue,dailyStartEpoch,availablepointEpoch)
            checkEqualAssert(flagBE,flag,message='Verify Snapping')

            if flagBE:
                expectedText=time_format(getDateString(dailyStartEpoch),getDateString(snapValue))
                checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],selectedQuicklink,message='Verify Snapped Value')
            else:
                expectedText = time_format(getDateString(dailyStartEpoch), getDateString(defaultRightValue))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

            udScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

        if '2592000' in availablepoint.keys():
            launchCalendar(setup, MRXConstants.UDPPOPUP)
            defaultRightValue=getDefaultRightCalendarValue(setup)
            dateStringStart = getDateString(monthlyStartEpoch, tPattern='%Y %B %d %H %M').split(' ')
            setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4], udScreenInstance,setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

            flag,value = isSnappingFromUI(setup)
            flagBE,snapValue=isSnapping(defaultRightValue,monthlyStartEpoch,availablepointEpoch)
            checkEqualAssert(flagBE,flag,message='Verify Snapping')
            if flagBE:
                expectedText=time_format(getDateString(monthlyStartEpoch),getDateString(snapValue))
                checkEqualAssert(formattedEndTime(getDateString(snapValue)),value[1],selectedQuicklink,message='Verify Snapped Value')
            else:
                expectedText = time_format(getDateString(monthlyStartEpoch), getDateString(defaultRightValue))

            valueFromCalender = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
            checkEqualAssert(expectedText,valueFromCalender,message='Verify TimeRange on Calendar')

            udScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

    ####################################################################################################################

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()