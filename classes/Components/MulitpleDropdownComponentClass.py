from DropdownComponentClass import DropdownComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *

class MulitpleDropdownComponentClass(DropdownComponentClass):

    def __init__(self):
        DropdownComponentClass.__init__(self)
        self.configmanager = ConfigManager()
        self.utility = __import__("Utils.utility")



    def getSelection(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        time.sleep(1)
        activeDropDowns[index].click()
        selections = []

        # for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
        #     for e in  el.find_elements_by_tag_name("input"):
        #         if str(e[0].get_attribute("checked")).upper() == "TRUE" or str(e[0].get_attribute("ng-reflect-checked")).upper() == "TRUE":
        #             selections.append(el.text)
        flag = False
        try:
            for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-model="true"],[ng-reflect-checked="true"]'):

                flag = True
                # commenting below lines to get all selected values in dropdown (Below if is only for Global Filter Scenario)
                if e.find_elements_by_xpath("../../div")[0].text.strip() == "Select All" or e.find_elements_by_xpath("../../div")[0].text.strip() == "All":
                    selections.append("ALL")
                    activeDropDowns[index].click()
                    return selections
                selections.append(e.find_elements_by_xpath("../../div")[0].text)
                # selections.append(e.find_elements_by_xpath("..//div")[0].text)
            if not flag:
                selections.append("")
        except Exception as e:
            try:
                for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-model="true"],[checked="true"]'):
                    flag=True
                    if e.find_elements_by_xpath("..//div")[0].text.strip() == "Select All":
                        selections.append("ALL")
                        activeDropDowns[index].click()
                        return selections
                    selections.append(e.find_elements_by_xpath("..//div")[0].text)
                if not flag:
                    selections.append("")
            except Exception as e:
                logger.error("Exception %s found while getting current selection, Component: MulitpleDropdownComponentClass",e)


        activeDropDowns[index].click()
        time.sleep(1)
        return selections

    def getSelectionWithIndex(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        selections = []

        # for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
        #     for e in  el.find_elements_by_tag_name("input"):
        #         if str(e[0].get_attribute("checked")).upper() == "TRUE" or str(e[0].get_attribute("ng-reflect-checked")).upper() == "TRUE":
        #             selections.append(el.text)
        try:

            for e in activeDropDowns[index].find_elements_by_css_selector('[ng-reflect-checked="true"]'):
                selections.append(e.find_elements_by_xpath("..//div")[0].text)
        except Exception as e:
            try:
                for e in activeDropDowns[index].find_elements_by_css_selector('[checked="true"]'):
                    selections.append(e.find_elements_by_xpath("..//div")[0].text)
            except Exception as e:
                logger.error("Exception %s found while getting current selection, Component: MulitpleDropdownComponentClass",e)

        return selections


    def domultipleSelection(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        time.sleep(2)
        for el in activeDropDowns[index].find_elements_by_class_name("menuitem"):
            if el.text == value:
                el.click()
        activeDropDowns[index].click()
        return self.getSelection(h,index)

    def setEqualOrNotEqualIcon(self,h,value,index,parent="filterPopup",child="multiselect-dropdown",setup=False,E_NE_index=1):
        try:
            activeDropDowns = self.getAllActiveElements(h[parent][child])
            activeDropDowns[index].click()
            time.sleep(2)
            if 'E' in value and 'not-equal' in activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].get_attribute('class'):
                activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].click()
            elif 'NE' in value and 'equal' in activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].get_attribute('class'):
                activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].click()
            elif not('E' in value) and not('NE' in value):
                return ''

            valueFromUI=str(activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].text)
            activeDropDowns[index].click()

            return valueFromUI
        except Exception as e:
            if setup != False:
                self.utility.utility.isError(setup)
            #raise e
            return e

    def getToggleStateInMultiDropDown(self,h,index,parent="filterPopup",child="multiselect-dropdown",setup=False,E_NE_index=1):
        try:
            activeDropDowns = self.getAllActiveElements(h[parent][child])
            activeDropDowns[index].click()
            time.sleep(2)

            togglevalue=str(activeDropDowns[index].find_elements_by_css_selector('i[class*=equalSignStyle]')[E_NE_index].text)
            activeDropDowns[index].click()

            return togglevalue
        except Exception as e:
            if setup != False:
                self.utility.utility.isError(setup)
            #raise e
            return e


    def domultipleSelectionWithIndex(self,h,value,index,parent="filterPopup",child="multiselect-dropdown",setup=False):
        try:
            activeDropDowns = self.getAllActiveElements(h[parent][child])
            activeDropDowns[index].click()
            time.sleep(2)
            elements = activeDropDowns[index].find_elements_by_css_selector('input[type="checkbox"]')
            #elements = activeDropDowns[index].find_elements_by_css_selector('div[class="menuitem"]')
            for i in range(len(elements)):
                if i in value or str(i) in value:
                    elements[i].click()

            activeDropDowns[index].click()
            return self.getSelection(h,index,parent,child)
        except Exception as e:
            if setup != False:
                self.utility.utility.isError(setup)
            raise e
            return e

    def getOptionsAvailable(self,h,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        return [el.text for el in activeDropDowns[index].find_elements_by_class_name("menuitem")]


    def doSearch(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = self.getAllActiveElements(h[parent][child])
        activeDropDowns[index].click()
        #for el in activeDropDowns[index].find_elements_by_class_name("input"):
        for el in activeDropDowns[index].find_elements_by_tag_name("input"):
            if el.get_attribute("type") == "text":
                el.send_keys(value)
                #return self.getOptionsAvailable(h,index)
                valueList=self.getOptionsAvailable(h,index)
                activeDropDowns[index].click()
                return valueList

    def getHeader(self,h,index,parent="picker",child="multiselect-dropdown"):
        return h[parent][child][index].find_elements_by_css_selector("[class*=PickerHeaderClass]")[0].text.strip().strip('\n').strip()


    def domultipleSelectionWithNameWithoutActiveDropDown(self,h,value,index,parent="filterPopup",child="multiSelectDropDown"):
        DropDowns = h[parent][child]

        for el in DropDowns[index].find_elements_by_class_name("menuitemDiv"):
            if str(el.text).strip() == value:
                el.click()
                return True


    def domultipleSelectionWithName(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = h[parent][child]
        activeDropDowns[index].click()
        time.sleep(5)

        for el in activeDropDowns[index].find_elements_by_class_name("menuitemDiv"):
            if str(el.text).strip() == value:
                el.click()
                return str(activeDropDowns[index].find_elements_by_xpath("./div/*")[0].text)

    def domultipleSelectionWithIndex_type2(self,h,value,index,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = h[parent][child]
        activeDropDowns[index].click()
        time.sleep(2)
        elements = activeDropDowns[index].find_elements_by_class_name("menuitemDiv")
        for i in range(len(elements)):
            if i == value:
                elements[i].click()
                return str(activeDropDowns[index].find_elements_by_xpath("./div/*")[0].text)

    def checkMeasureInActiveList(self,h,value,index,parent="filterPopup",child="multiselect-dropdown",strToBeReplaced='Flow',strToBeReplacedWith='Hit'):
        activeDropDowns = h[parent][child]
        activeDropDowns[index].click()
        time.sleep(5)

        if strToBeReplaced in value:
            for el in activeDropDowns[index].find_elements_by_class_name("menuitemDiv"):
                if strToBeReplaced in str(el.text).strip():
                    activeDropDowns[index].click()
                    return value
            activeDropDowns[index].click()
            return str(value).replace(strToBeReplaced,strToBeReplacedWith)
        activeDropDowns[index].click()
        return value


    def domultipleSelectionWithIndex_type2_random(self,h,occurence=0,parent="filterPopup",child="multiselect-dropdown"):
        activeDropDowns = h[parent][child]
        activeDropDowns[occurence].click()
        time.sleep(2)
        elements = activeDropDowns[occurence].find_elements_by_class_name("menuitemDiv")
        try:
            import  random
            indexToBeSelected = random.randint(0,len(elements)-1)
        except ValueError or Exception as e:
            logger.error("Exception found (No options available) for selection in DropDown = %s",str(e))
            return "Exception :"+str(e)
        for i in range(len(elements)):
            if i == indexToBeSelected:
                elements[i].click()
                return str(activeDropDowns[occurence].find_elements_by_xpath("./div/*")[0].text)