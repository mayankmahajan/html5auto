from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *
from selenium.common.exceptions import *

from classes.Components.DropdownComponentClass import *


class CalendarComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()



    # SetCalendar
    def setCalendar(self,year,month,day,hour,minute,h,parent="leftcalendar"):
        try:
            self.set("year",year,h,parent)
            self.set("month",month,h,parent)
            self.setDay("day",day,h,parent)

        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            return e


    def set(self,child,year,h,parent="leftcalendar"):
        try:
            dropDown = DropdownComponentClass()
            return dropDown.doSelectionOnVisibleDropDown(h,year,0,parent,child)
            # dropDown.doSelection(h,year,parent,child)
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            return e

    def setDay(self,child,day,h,parent="leftcalendar"):
        try:
            availableDates = self.getAvailableDates(h[parent][child])
            self.selectDay(day,availableDates)
            return True
            # will handle below code later

            daySelection =  self.getDaySelection(h,parent,child)

            if daySelection != []:
                return daySelection[0].text
            else:
                return "No Selection present"
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            return e


    def getAvailableDates(self,h):
        dates = self.getAllDates(h, "tbody", "td")
        availableDates = []
        for el in dates:
            if "available" in el.get_attribute("class"):
                availableDates.append(el)
        return availableDates

    def selectDay(self,day,availableDates):
        for el in availableDates:
            if el.text == day:
                el.click()



        # for i in range(len(availableDates)):
        #     previousDay = availableDates[i].text if i==0 else availableDates[i-1].text
        #     if int(previousDay)> int(availableDates[i].text):
        #         break
        #     if availableDates[i].text == day:
        #         availableDates[i].click()
        #         logger.info("Selected Day is  : %s",str(day))
        #         return True
        #
        # logger.error("Day is not available for selection : %s",str(availableDates[i].text))
        # return False


    def getAllDates(self, h, tbody, td):
        return h[0].find_elements_by_tag_name(tbody)[0].find_elements_by_tag_name(td)
        # return h.find_elements_by_tag_name(tbody)[0].find_elements_by_tag_name(td)

    def getDaySelection(self,h,parent,child="day"):
        dates = self.getAllDates(h[parent][child], "tbody", "td")
        for d in dates:
            if "active" in d.get_attribute("class"):
                return d
        return []



