from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time

class DropdownComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

    def doSelection(self,h,value,parent,child=None):
        self.set(value, h[parent][child])

    def set(self, value, handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == value:
                ele.click()
                break
