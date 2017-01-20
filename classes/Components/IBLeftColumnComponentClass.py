from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *
from selenium.common.exceptions import *

class IBLeftColumnComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def select(self,index,h,parent=None,child=None):
        try:
            if parent==None:
                parent='leftcolumn'
            if child==None:
                child='columns'

            leftlinks = h[parent][child][len(h[parent][child])-1].find_elements_by_tag_name("button")
            for i in range(len(leftlinks)):
                if index == i:
                    leftlinks[i].click()
                    return True
            return True
        except ElementNotSelectableException or NoSuchElementException or ElementNotVisibleException or StaleElementReferenceException or Exception as e:
            return e


