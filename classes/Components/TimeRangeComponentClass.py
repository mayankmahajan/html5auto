#!/usr/bin/env python
##############################################################
'''
QuickLink TimeRange Component Handler
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################

from QuicklinkTimeRangeComponentClass import QuicklinkTimeRangeComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *

from selenium.webdriver import ActionChains
from Utils.utility import *
from Utils.ConfigManager import *
from classes.Objects.Time import *



class TimeRangeComponentClass(QuicklinkTimeRangeComponentClass):

    def __init__(self):
        QuicklinkTimeRangeComponentClass.__init__(self)

    def setCustomTime(self,date,h,parent="timeRangeDiv",child="cal"):

        # Activate
        h[parent][child][len(h[parent][child])-1].click()

    def isCompleteDay(self,str):
        if int(str.split(" ")[1].split(":")[0]) == 0:
            return True
        else:
            return False

    def getAllquicklinkLable(self,flag=Constants.FLAGHOURLY,stEtCombID=0):
        qs = self.configmanager.getNodeElements("wizardquicklinks1", "wizardquicklink")
        qList = self.configmanager.getAllNodeElements("wizardquicklinks1", "wizardquicklink")
        allquicklink={}
        for e in qList:
            allquicklink[e] =TimeRangeComponentClass().getLabel(e, flag,stEtCombID=stEtCombID)
        return allquicklink

    def time_format(self,starttime,endtime):
        if starttime.split(" ")[3].split(":")[0]=='00' and endtime.split(" ")[3].split(":")[0]=='00':
            endtimeEpoch=getepoch(endtime)
            endtimeEpoch=endtimeEpoch-3600
            endtime=getDateString(endtimeEpoch)
            return starttime.split(" ")[0] + " " + starttime.split(" ")[1] + " " + starttime.split(" ")[2] + " to " + endtime.split(" ")[0] + " " + endtime.split(" ")[1] + " " + endtime.split(" ")[2]
        else:
            return starttime+" to "+endtime

    def get_Label(self, quicklink, flag=Constants.FLAGHOURLY, stEtCombID=0):

        st = self.configmanager.getNodeElements("availabletimerange", "starttime")[str(stEtCombID)]
        et = self.configmanager.getNodeElements("availabletimerange", "endtime")[str(stEtCombID)]

        # st = self.configmanager.getNodeElements("availabletimerange", "starttime")['starttime']
        # et = self.configmanager.getNodeElements("availabletimerange", "endtime")['endtime']

        stime = Time(st['year'], st['month'], st['day'], st['hour'],st['min'])
        etime = Time(et['year'], et['month'], et['day'], et['hour'],et['min'])

        stepoch = getepoch(stime.datestring, Constants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")
        etepoch = getepoch(etime.datestring, Constants.TIMEZONEOFFSET, "%Y-%m-%d %H:%M")

        stime1=getDateString(stepoch,tPattern ='%d %b %Y %H:%M')
        etime1=getDateString(etepoch,tPattern ='%d %b %Y %H:%M')

        # h = time.strftime('%H', time.localtime(etepoch - 3600 * Constants.TIMEZONE))
        # h1 = time.strftime('%H', time.localtime(stepoch - 3600 * Constants.TIMEZONE))
        # ds = time.strftime('%A', time.localtime(etepoch - 3600 * Constants.TIMEZONE))
        # d = time.strftime('%d', time.localtime(etepoch - 3600 * Constants.TIMEZONE))
        # m = time.strftime('%m', time.localtime(etepoch - 3600 * Constants.TIMEZONE))

        h = getDateString(etepoch,tPattern='%H')
        h1 = getDateString(stepoch, tPattern='%H')
        ds = getDateString(etepoch, tPattern='%A')
        d = getDateString(etepoch, tPattern='%d')
        m = getDateString(etepoch, tPattern='%m')

        if quicklink == "today" :
            if int(h) == 0:
                h=24
            if (etepoch - stepoch)<= int(h)*3600 :
                return True, self.time_format(stime1,etime1)
            else:
                return True, self.time_format(getDateString(etepoch-3600*int(h),tPattern ='%d %b %Y %H:%M'),etime1)

        elif quicklink == "yesterday":
            if int(h) == 0:
                h=24
            if (etepoch - stepoch) <= int(h)*3600:
                return False,""
            else:
                    if (etepoch - stepoch) > (int(h)+24)*3600 :
                        return True, getDateString(etepoch-(3600*(int(h)+24)),tPattern ='%d %b %Y')
                    else:
                        return True, self.time_format(stime1,getDateString(etepoch-3600*int(h)))

        elif quicklink=="last7days":
            if int(h) == 0:
                h=24
            if (etepoch - stepoch) <= int(h)*3600:
                return False,""
            else:
                    if (etepoch - stepoch) > (int(h)+(24*7))*3600 :
                        return True, self.time_format(getDateString(etepoch-(3600*(int(h)+(24*7)))),getDateString(etepoch-(3600*(int(h)))))
                    else:
                        return True, self.time_format(stime1,getDateString(etepoch-(3600*(int(h)))))

        elif quicklink=="last30days":
            if int(h) == 0:
                h=24
            if (etepoch - stepoch) <= int(h)*3600:
                return False,""
            else:
                    if (etepoch - stepoch) > (int(h)+(24*30))*3600 :
                        return True, self.time_format(getDateString(etepoch-(3600*(int(h)+(24*30)))),getDateString(etepoch-(3600*(int(h)))))
                    else:
                        return True, self.time_format(stime1,getDateString(etepoch-(3600*(int(h)))))


        elif quicklink=="last4hours":
            if (etepoch - stepoch) <= 4*3600:
                return True, self.time_format(stime1, etime1)
            else:
                return True, self.time_format(getDateString(etepoch-(3600*4)),etime1)

        elif quicklink=="last24hours":
            if (etepoch - stepoch) <= 24*3600:
                return True, self.time_format(stime1, etime1)
            else:
                return True, self.time_format(getDateString(etepoch-(3600*24)),etime1)

        elif quicklink == "thisweek":
            numberofdayfromsunday = int(dayNameToNumber[ds])
            oldh=int(h)
            oldh1 = int(h1)

            if int(h) ==0:
                h=24
                h1=24
                numberofdayfromsunday = numberofdayfromsunday - 1
            else:
                h=oldh
                h1=oldh1

            if (etepoch - stepoch)>= ((numberofdayfromsunday - 1)*24 + int(h))*3600:
                if flag==Constants.FLAGHOURLY:
                    return True,self.time_format(getDateString(etepoch - ((numberofdayfromsunday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'),etime1)
                elif flag==Constants.FLAGDAILY:
                    if oldh !=0:
                        return True, self.time_format(getDateString(etepoch - ((numberofdayfromsunday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - int(h)*3600,tPattern ='%d %b %Y %H:%M'))
                    else:
                        return True,self.time_format(getDateString(etepoch - ((numberofdayfromsunday - 1) * 24 + int(h)) * 3600,tPattern ='%d %b %Y %H:%M'),etime1)
            else:
                if flag==Constants.FLAGHOURLY:
                    return True,self.time_format(stime1,etime1)
                elif flag==Constants.FLAGDAILY:
                    f1=self.isCompleteDay(stime.datestring)
                    f2 = self.isCompleteDay(etime.datestring)

                    if f1==True and f2==True:
                        return True, self.time_format(stime1,etime1)
                    elif f1==True and f2==False:
                        if int(h)!=0:
                            return True, self.time_format(stime1,getDateString(etepoch - int(h)*3600,tPattern ='%d %b %Y %H:%M'))
                        else:
                            return True, self.time_format(stime1,etime1)

                    elif f2==True and f1== False:
                        return True, self.time_format(getDateString(stepoch + (24-int(h1))*3600,tPattern ='%d %b %Y %H:%M'),etime1)
                    else:
                        if int(h) != 0:
                            return True, self.time_format(getDateString(stepoch + (24 - int(h1)) * 3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - int(h)* 3600,tPattern ='%d %b %Y %H:%M'))
                        else:
                            return True, self.time_format(getDateString(stepoch + (24-int(h1))*3600,tPattern ='%d %b %Y %H:%M'),etime1)

        elif quicklink == "thismonth":
            numberofday = int(d)
            oldh=int(h)
            oldh1=int(h1)
            if int(h)==0:
                h=24
                numberofday= numberofday - 1
            else:
                h=oldh
                h1=oldh1

            if (etepoch - stepoch)>= ((numberofday - 1)*24 + int(h))*3600:
                if flag==Constants.FLAGHOURLY:
                    return True, self.time_format(getDateString(etepoch - ((numberofday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'),etime1)
                elif flag==Constants.FLAGDAILY:
                    return True, self.time_format(getDateString(etepoch - ((numberofday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - int(h)*3600,tPattern ='%d %b %Y %H:%M'))
            else:
                if flag==Constants.FLAGHOURLY:
                    return True, self.time_format(stime1,etime1)
                elif flag==Constants.FLAGDAILY:
                    f1 = self.isCompleteDay(stime.datestring)
                    f2 = self.isCompleteDay(etime.datestring)

                    if f1 == True and f2 == True:
                        return True, self.time_format(stime1,etime1)
                    elif f1 == True and f2 == False:
                        return True, self.time_format(stime1,getDateString(etepoch - int(h) * 3600,tPattern ='%d %b %Y %H:%M'))
                    elif f2 == True and f1 == False:
                        return True,self.time_format(getDateString(stepoch + (24 -int(h1)) * 3600,tPattern ='%d %b %Y %H:%M'),etime1)
                    else:
                        return True, self.time_format(getDateString(stepoch + (24 -int(h1)) * 3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - int(h)*3600,tPattern ='%d %b %Y %H:%M'))
        elif quicklink == "lastweek":
            numberofdayfromsunday = int(dayNameToNumber[ds])
            if int(h) == 0:
                h = 24
                numberofdayfromsunday = numberofdayfromsunday - 1
            if (etepoch - stepoch)>= ((numberofdayfromsunday - 1)*24 + int(h))*3600:

                if (etepoch - stepoch)>= ((7+numberofdayfromsunday - 1)*24 + int(h))*3600:
                    return True, self.time_format(getDateString(etepoch - ((7+numberofdayfromsunday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - ((numberofdayfromsunday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'))
                else:
                    return True, self.time_format(stime1,getDateString(etepoch - ((numberofdayfromsunday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'))
            else:
                return False,""

        elif quicklink == "lastmonth":
            numberofday = int(d)
            if int(h) == 0:
                h = 24
                numberofday = numberofday - 1

            if (etepoch - stepoch)>= ((numberofday - 1)*24 + int(h))*3600:
                if (int(m) - 1 ) == 0:
                    month= str('12')
                else:
                    month=str(int(m)-1)

                if (etepoch - stepoch) >= ((int(dayinmonth[month]) + int(d) - 1) * 24 + int(h)) * 3600:
                    return True, self.time_format(getDateString(etepoch - ((int(dayinmonth[month]) + numberofday - 1) * 24 + int(h)) * 3600,tPattern ='%d %b %Y %H:%M'),getDateString(etepoch - ((numberofday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'))
                else:
                    return True,self.time_format(stime1,getDateString(etepoch - ((numberofday - 1)*24 + int(h))*3600,tPattern ='%d %b %Y %H:%M'))
            else:
                return False, ""

        else:
            return False,""




    @staticmethod
    def getLabel(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to get TimeRange Label from KTRS")
            label= str(h[parent][child][0].find_elements_by_xpath("./*")[0].text)
            logger.info("Got TimeRange Label from KTRS = %s",label)
            return label
        except Exception as e:
            logger.error("Got Exception while getting selection label from KTRS = %s",str(e))
            return e

    @staticmethod
    def launchCalendar(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to launch Calendar from KTRS")
            h[parent][child][0].find_elements_by_xpath("./*")[1].click()
            logger.info("Launch Calendar icon clicked successfully")
            return True
        except Exception as e:
            logger.error("Got Exception while clicking Calendar icon from KTRS = %s",str(e))
            return e


    @staticmethod
    def setQuickLink(value,h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to click quicklink from KTRS = %s",str(value))
            quicklinkHandlers = h[parent][child][0].find_elements_by_xpath("./*")[2]
            quickLinkToClick = quicklinkHandlers.find_elements_by_xpath('//a[contains(text(), "' + value + '")]')
            logger.info("Got Quicklink(s) with text = %s on the KTRS = %d ",str(value),len(quickLinkToClick))
            logger.info("Going to click on Quicklink = %s",str(quickLinkToClick[0].text))
            quickLinkToClick[0].click()
            logger.info("Quicklink clicked successfully")
            return True
        except Exception as e:
            logger.error("Got Exception while clicking quicklink = %s from KTRS = %s",str(value),str(e))
            return e

    @staticmethod
    def getSelectedQuickLink(h,parent="ktrs",child="bar"):
        try:
            logger.info("Going to getSelectedQuickLink from KTRS")
            quicklinkHandlers = h[parent][child][0].find_elements_by_xpath("./*")[2]
            selectedQuickLink = str(quicklinkHandlers.find_elements_by_css_selector("a[class=timeRangeSelectedText]")[0].text)
            logger.info("Got SelectedQuickLink from KTRS = %s",selectedQuickLink)
            return selectedQuickLink
        except Exception as e:
            logger.error("Got Exception while fetching Selected Quicklink = %s",str(e))
            return e


    def getAvailableTimeRange(self):
        st = self.configmanager.getNodeElements("availabletimerange","starttime")
        et = self.configmanager.getNodeElements("availabletimerange","endtime")
        return st,et