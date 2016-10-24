from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager

class MeasureComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def doSelection(self,h,measure):
        handlers = self.compHandlers('primaryMeasure',h)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "click":
                self.setMeasure(measure,value)


# handlers['primaryMeasure'][0].find_element_by_xpath("//option[text()='Flows']").click()

    def setMeasure(self,measure,handle):
        meaurePath="//option[text()='" + measure + "']"
        handle[0].find_element_by_xpath(meaurePath).click()


