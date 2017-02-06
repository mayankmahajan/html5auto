from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *

class MeasureComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def doSelection(self,h,measure):
        try:
            handlers = self.compHandlers('measureselectors',h)
            measureArr=measure.split("_")
            measureName=measureArr[0]
            downUpTotal=measureArr[1]
            absPerc=measureArr[2]

            # Setting Measure name like bitrate,tonnage,etc.
            self.setMeasureName(measureName,handlers['primaryMeasure'])
            logger.debug("Selecting the measures :: Measurename :- %s  Down/UP/Total :- %s  Abs/Per :- %s ",measureName,downUpTotal,absPerc)
            # Setting Downlink,Uplink,Total
            self.select(handlers[downUpTotal])

            # Setting Absolute,Percentage
            time.sleep(2)
            self.select(handlers[downUpTotal])
            time.sleep(2)
            self.select(handlers[absPerc])
            time.sleep(2)
            try:
                avgPeak=measureArr[3]
                logger.debug("Selecting the measure avg/peak :- %s",avgPeak)
                self.select(handlers[avgPeak])
            except:
                logger.debug("Got Measure without Peak/Average %s",measureName)
                print "Got Measure without Peak/Average %s",measureName
            return True
        except Exception as e:
            logger.debug("Exception found while selecting the measures %s %s %s %s",measureName,downUpTotal,absPerc,avgPeak)
            logger.error("Exception found while selecting the measures",e)
            return e


    def doSelectionSite1(self,h,site,parent="measureselectors"):
        handlers = self.compHandlers(parent,h)
        sitename = site
        self.setSiteName(sitename,handlers['sites'])

    def doSelectionSite(self,h,site,parent="measureselectors"):
        handlers = h[parent]
        sitename = site
        self.setSiteName(sitename,handlers['sites'])


    def setSiteName(self,site,handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == site:
                ele.click()
                break



    def setMeasureName(self,measure,handle):
        for ele in handle[len(handle)-1].find_elements_by_xpath(".//*"):
            if ele.text == measure:
                ele.click()
                break

    def select(self,handle):
        handle[len(handle)-1].click()
        time.sleep(1)
