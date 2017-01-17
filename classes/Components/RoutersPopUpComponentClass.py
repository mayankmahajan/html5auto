from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *
from selenium.common.exceptions import *
from classes.Components.DropdownComponentClass import *
from Utils.utility import *




class RoutersPopUpComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    # def setQueryName(self,value,h,parent,child):
    #     h1 = h[parent][child]
    #     pass

# h1[0].find_elements_by_tag_name("ag-grid-ng2")[0].find_elements_by_class_name("ag-selection-checkbox")

    def setQueryName(self,value,h,parent,child):
        try:
            h[parent][child][len(h[parent][child])-1].find_elements_by_tag_name("input")[0].send_keys(value)
            return h[parent][child][len(h[parent][child])-1].find_elements_by_tag_name("input")[0].get_attribute("value")
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e
            return e

    def getQueryName(self,value,h,parent,child):
        try:
            return h[parent][child][len(h[parent][child])-1].find_elements_by_tag_name("input")[0].get_attribute("value")
        except StaleElementReferenceException or ElementNotVisibleException or NoSuchElementException or Exception as e:
            raise e
            return e


# h1[0].find_elements_by_tag_name("table")[0].find_elements_by_tag_name('td')[1].find_elements_by_tag_name("select")[0]

    def getHandler(self,index,h):
        return h.find_elements_by_tag_name("table")[0].find_elements_by_tag_name('td')[index]

    def setTime(self,index,h,parent,child,setup,date=None):

        try:
            if index != 0:
                index = 2
            handle = self.getHandler(index,h[parent][child][len(h[parent][child])-1])
            handle.find_elements_by_tag_name("img")[0].click()

            if index==2:
                index = 1
            # will call calendar selection here using 'date' argument
            self.doCalendarSelection(setup,parent,index,date)

            # handle.find_elements_by_tag_name("img")[0].click()
            return handle.find_elements_by_tag_name("input")[0].get_attribute("value")
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e
            return e


    def setTime2(self,index,h,parent,child,setup,date=None):

        try:
            if index != 0:
                index = 2
            handle = self.getHandler(index,h[parent][child][len(h[parent][child])-1])
            handle.find_elements_by_tag_name("img")[0].click()

            if index==2:
                index = 1
            # will call calendar selection here using 'date' argument
            self.doCalendarSelection(setup,parent,index,date)

            # handle.find_elements_by_tag_name("img")[0].click()
            return handle.find_elements_by_tag_name("input")[0].get_attribute("value")
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e
            return e

    def setTime1(self,index,h,parent,child,setup,date=None):

        try:
            if index != 0:
                index = 2
            handle = self.getHandler(index,h[parent][child][len(h[parent][child])-1])
            handle.find_elements_by_tag_name("img")[0].click()

            # will call calendar selection here using 'date' argument
            self.doCalendarSelection(setup,parent,index,date)

            # handle.find_elements_by_tag_name("img")[0].click()
            return handle.find_elements_by_tag_name("input")[0].get_attribute("value")
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e
            return e

    def getTime(self,index,h,parent,child):
        if index != 0:
            index = 2
        handle = self.getHandler(index,h[parent][child][len(h[parent][child])-1])
        return handle.find_elements_by_tag_name("input")[0].get_attribute("value")


    def setSortBy(self,value,h,parent,child):
        self.select(1,value,h,parent,child)
        return True

    def setSortOrder(self,value,h,parent,child):
        self.select(3,value,h,parent,child)
        return True

    def setPageSize(self,value,h,parent,child):
        self.select(4,value,h,parent,child)
        return True

    def select(self,i,value,h,parent,child):
        try:
            handle = self.getHandler(i,h[parent][child][len(h[parent][child])-1])
            d = DropdownComponentClass()
            d.set(value,handle.find_elements_by_tag_name("select"))
            return True
        except NoSuchElementException or StaleElementReferenceException or ElementNotVisibleException or Exception as e:
            raise e
            return e


    def doCalendarSelection(self,setup,parent,index,date=None):
        hParent = getHandle(setup,"routers_popup")[parent]

        for el in hParent['calendar'][index].find_elements_by_tag_name("button"):
            if 'apply' in el.get_attribute("class"):
                try:
                    el.click()
                    return True
                except NoSuchElementException or ElementNotSelectableException or Exception as e:
                    return e




    def addGroup(self,index,handle,parent="wizard2",child="qp"):
        handler = handle[parent][child]
        for ele in handler.find_elements_by_tag_name("button"):
            if ele.text == "Add Group":
                ele.click()
                break




    def addRule(self,index,handle):
        pass