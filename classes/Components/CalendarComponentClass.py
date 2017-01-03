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
            self.set("year",year,parent,h)
            self.set("month",year,parent,h)
            self.setDay("day",day,parent,h)

        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            return e


    def set(self,child,year,parent,h):
        try:
            dropDown = DropdownComponentClass()
            dropDown.doSelection(h,year,parent,child)
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            return e

    def setDay(self,child,day,parent,h):
        try:
            availableDates = self.getAvailableDates(h[parent][child])
            self.selectDay(day,availableDates)
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

    def getAllDates(self, h, tbody, td):
        return h.find_elements_by_tag_name(tbody)[0].find_elements_by_tag_name(td)

    def getDaySelection(self,h,parent,child="day"):
        dates = self.getAllDates(h[parent][child], "tbody", "td")
        for d in dates:
            if "active" in d.get_attribute("class"):
                return d
        return []



