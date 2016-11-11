from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time

class MeasureComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def doSelection(self,h,measure):
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


        #
        #
        #
        # for key,value in handlers.iteritems():
        #     if self.configmanager.componentSelectors[key]["action"] == "click":
        #         self.setMeasure(measure,value)


# handlers['primaryMeasure'][0].find_element_by_xpath("//option[text()='Flows']").click()

    # def setMeasureName(self,measure,handle):
    #     meaurePath="//option[text()='" + measure + "']"
    #     handle[0].find_element_by_xpath(meaurePath).click()
    #
    # def select(self,handle):
    #     handle[0].click()
    #     time.sleep(1) #Sets 1 second delay so as to make sure Main Charts drawn properly

    def setMeasureName(self,measure,handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == measure:
                ele.click()
                break
        # meaurePath="//option[text()='" + measure + "']"
        # handle[len(handle)-1].find_element_by_xpath(meaurePath).click()

    def select(self,handle):
        handle[len(handle)-1].click()
        time.sleep(1)
