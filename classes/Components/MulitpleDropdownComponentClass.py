from DropdownComponentClass import DropdownComponentClass
from Utils.ConfigManager import ConfigManager
import time

class MulitpleDropdownComponentClass(DropdownComponentClass):

    def __init__(self):
        DropdownComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getAllActiveDropdowns(self,childHandles):
        activeElements = []
        for ele in childHandles:
            # 'disabled' not in ele.get_attribute("class") and
            if ele.is_displayed():
                activeElements.append(ele)
            else:
                pass
        return activeElements


    def getSelection(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveDropdowns(h[parent][child])
        activeDropDowns[index].click()
        selections = []

        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            for e in  el.find_elements_by_tag_name("input"):
                if e.get_attribute("checked") == True:
                    selections.append(el.text)

        return selections

    def domultipleSelection(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveDropdowns(h[parent][child])
        activeDropDowns[index].click()
        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            if el.text == value:
                el.click()

        return self.getSelection(h,index)

    def getOptionsAvailable(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveDropdowns(h[parent][child])
        return [el.text for el in activeDropDowns[index].find_elements_by_class_name("menuitem")]


    def doSearch(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveDropdowns(h[parent][child])
        activeDropDowns[index].click()
        for el in activeDropDowns[index].find_elements_by_class_name("input"):
            if el.get_attribute("type") == "text":
                el.send_keys(value)
        return self.getOptionsAvailable(h,index)

    def doSelection(self,h,value,parent,child=None):
        self.set(value, h[parent][child])

    def set(self, value, handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == value:
                ele.click()
                break
