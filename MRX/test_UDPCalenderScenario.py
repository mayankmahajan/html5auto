from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from Utils.SetUp import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import random

def launchCalendar(setup,Page,parent='ktrs',child='datepicker',index=0):
    calHandler = getHandle(setup, Page,parent)
    logger.info("Launching Calendar: ")
    calHandler[parent][child][index].click()
    logger.info("Calendar picker is clicked")

try:
    setup = SetUp()
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    udScreenInstance = UDScreenClass(setup.d)
    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")

    UDHelper.clearFilter(setup, MRXConstants.UDSCREEN)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.UDSCREEN, 'nofilterIcon')

    launchCalendar(setup,MRXConstants.UDPPOPUP)

    st = ConfigManager().getNodeElements("availabletimerange", "starttime")[str(0)]
    et = ConfigManager().getNodeElements("availabletimerange", "endtime")[str(0)]

    stime = Time(st['year'], st['month'], st['day'], st['hour'], st['min'])
    etime = Time(et['year'], et['month'], et['day'], et['hour'], et['min'])

    stepoch = getepoch(stime.datestring, MRXConstants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")
#    etepoch = getepoch(etime.datestring, MRXConstants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")

    valueFromCalenderBeforeSelectingPastDate = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()

    dateStringStart = getDateString(stepoch-86400, tOffset=MRXConstants.TIMEZONEOFFSET,tPattern='%Y %B %d %H %M').split(' ')
    setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")


    valueFromCalenderAfterSelectingPastDate = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
    checkEqualAssert(True,str(valueFromCalenderBeforeSelectingPastDate).strip()==str(valueFromCalenderAfterSelectingPastDate).strip(),message='Verify Past date disable on Calendar',testcase_id='MKR-3190')
    udScreenInstance.clickButton("Cancel", getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))

    launchCalendar(setup, MRXConstants.UDPPOPUP)
    valueFromCalenderBeforeSelectingFutureDate = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
    dateStringStart = getDateString(stepoch + 86400, tOffset=MRXConstants.TIMEZONEOFFSET,tPattern='%Y %B %d %H %M').split(' ')
    setCalendar(dateStringStart[0], dateStringStart[1], dateStringStart[2], dateStringStart[3], dateStringStart[4],udScreenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")

    valueFromCalenderAfterSelectingFutureDate = str(getHandle(setup, Constants.CALENDERPOPUP, 'allspans')['allspans']['span'][0].text).strip()
    checkEqualAssert(True, str(valueFromCalenderBeforeSelectingFutureDate).strip() == str(valueFromCalenderAfterSelectingFutureDate).strip(), message='Verify Past date disable on Calendar',testcase_id='MKR-3190')

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()