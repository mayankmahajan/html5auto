from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
class BTVComponentClass(BaseComponentClass):

    def getDataforColumn1(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getDataForColumn2(self,elHandle):
        return [eachHandler.text for eachHandler in elHandle]

    def getData(self,h1,h2,h3):
        c1 = self.getDataforColumn1(h2)
        c2 = self.getDataForColumn2(h3)
        data = dict(zip(c1,c2))
        return data
