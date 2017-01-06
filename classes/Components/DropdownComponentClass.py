from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time

class DropdownComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

    def doSelection(self,h,value,parent,child=""):
        self.set(value, h[parent][child])

    def set(self, value, handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == value:
                ele.click()
                break


    def doSelectionOnVisibleDropDown(self,h,value,index=0,parent="allselects",child="select"):
        activedrops  = self.getAllActiveElements(h[parent][child])
        self.set(value, activedrops[index])

