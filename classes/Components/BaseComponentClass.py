# from classes.DriverHelpers.DriverHelper import DriverHelper
# from selenium import webdriver
# webdriver.Firefox().find_element_by_xpath().send_keys()
from Utils.UnitSystem import UnitSystem
from Utils.ConfigManager import ConfigManager

class BaseComponentClass:
    def m_click(self,elHandle):
        return elHandle.click()
    def m_send_keys(self,elHandle,value):
        return elHandle.send_keys(value)
    def text(self,elHandle):
        return elHandle.text

    def getSelection(self):
        '''
        Base method for getSelection that can be used across all components for uniformity
        :return: Selection
        '''
        selection = []
        return selection

    def getSpecificLocators(self,locatorClass):
        '''
        Can be overridden at ComponentClass
        :param locatorClass: Locator Class of Component
        :return: component child as Key and its locators as Value
        '''
        return self.dictionary_ele_locators(locatorClass)

    def dictionary_ele_locators(self, locatorClass):
        dic = {}
        for method in dir(locatorClass):
            if type(getattr(locatorClass,method)) == tuple:
                dic[method]= getattr(locatorClass,method)
        return dic

    def validateToolTipData(self,dataCollection):
        result = {}
        return result

    def compare(self,v1,v2):
        if v1 == v2:
            return True
        else:
            return False

    def __init__(self):
        self.unitSystem = UnitSystem()
        self.configmanager = ConfigManager()


    def compHandlers(self,comp,handlers):
        newHandlers = {}
        for k,v in handlers.iteritems():
            if k in self.configmanager.componentChildRelations[comp]:
                newHandlers[k] = v
        return newHandlers


    def selectDropDownByText(self,handler,text,text2="HAHA"):
        for ele in handler.find_elements_by_xpath(".//*"):
            if ele.text == text or ele.text == text2:
                ele.click()
                return ele.text

    def doSelection(self,h,parentLocator,measure):
        handlers = self.compHandlers('measureselectors',h)
        measureArr=measure.split("_")
        measureName=measureArr[0]
        downUpTotal=measureArr[1]
        absPerc=measureArr[2]
        self.setMeasureName(measureName,handlers['primaryMeasure'])
        self.select(handlers[downUpTotal])
        self.select(handlers[absPerc])
        try:
            avgPeak=measureArr[3]
            self.select(handlers[avgPeak])
        except:
            print "Got Measure without Peak/Average %s",measureName




