from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
class BTVComponentClass(BaseComponentClass):

    def getDataforColumn1(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getDataForColumn2(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getSelection(self):
        selection= [];
        return selection

    def totalCheck(self,handlers):
        return True

    def getData(self,handlers):
        c1 = self.getDataforColumn1(handlers[Constants.BTVCOLUMN1])
        c2 = self.getDataForColumn2(handlers[Constants.BTVCOLUMN2])
        data = dict(zip(c1,c2))
        return data

    # def getSpecificLocators(self):
    #     return self.dictionary_ele_handlers(BTVLocators)
        # specific_elements = [Constants.BTV, Constants.BTVCOLUMN0, Constants.BTVCOLUMN1, Constants.BTVCOLUMN2]
        # specific_locators = [BTVLocators.BTV, BTVLocators.BTVCOLUMN0, BTVLocators.BTVCOLUMN1, BTVLocators.BTVCOLUMN2]
        # return dict(zip(specific_elements,specific_locators))
