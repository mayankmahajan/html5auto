from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.ConfigManager import ConfigManager

class BTVComponentClass(BaseComponentClass):

    def __init__(self):
        self.configmanager = ConfigManager()


    def getDataforColumn(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def setSelectionIndex(self,index,elHandle):
        for i in range(1,len(elHandle)):
            if i == index:
                elHandle[i].click()
                break


        # return [eachHandler.click for eachHandler in elHandle]

    def getDataforColumn1(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getDataForColumn2(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getSelectionIndex(self,elHandle):
        for i in range(1,len(elHandle)):
            if "255" not in elHandle[i].value_of_css_property('background-color') :
                return i


    def totalCheck(self,handlers):
        return True

    def getData1(self,handlers):
        c1 = self.getDataforColumn1(handlers[Constants.BTVCOLUMN1])
        c2 = self.getDataForColumn2(handlers[Constants.BTVCOLUMN2])
        data = dict(zip(c1,c2))
        return data

    def getData(self,handlers):
        data = {}
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "getData":
                data[key] = self.getDataforColumn(value)
        return data

    def setSelection(self,index,handlers):
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "click":
                self.setSelectionIndex(index,value)
        # return data

    def getSelection(self,handlers):
        data = {}
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "click":
                data['selIndex'] = self.getSelectionIndex(value)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "getData":
                data[key] = value[data['selIndex']].text
        return data

    # def getSpecificLocators(self):
    #     return self.dictionary_ele_handlers(BTVLocators)
        # specific_elements = [Constants.BTV, Constants.BTVCOLUMN0, Constants.BTVCOLUMN1, Constants.BTVCOLUMN2]
        # specific_locators = [BTVLocators.BTV, BTVLocators.BTVCOLUMN0, BTVLocators.BTVCOLUMN1, BTVLocators.BTVCOLUMN2]
        # return dict(zip(specific_elements,specific_locators))
