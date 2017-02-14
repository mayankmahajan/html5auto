from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *

class AlertsComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getAlertList(self,h,parent,child):
        list = {}
        for row in h[parent][child]:
            temp = self.createAlertListObject(row)
            list[temp['header']+"$$"+temp['duration']] = temp
        return list


    def selectAlert(self,index,h,parent,child):
        try:
            h[parent][child][index].click()
        except:
            return False


    def getSelectedAlert(self,h,parent,child):
        return self.getAlertList(h,parent,child)

    def createAlertListObject(self,h):
        alertObject={}
        alertObject['handled'] = self.getAlertHandledIcon(h)
        alertObject['header'] = self.getAlertLabels(h)[0]
        alertObject['duration'] = self.getAlertLabels(h)[1]
        alertObject['alarms'] = self.getAlertLabels(h)[2]
        alertObject['measure'] = self.getAlertLabels(h)[3]
        alertObject['color'] = self.getThresholdIconColor(h)
        return alertObject

    def getAlertHandledIcon(self,h):
        return False if "UnHandled".upper() in h.find_element_by_tag_name("img").get_attribute("class").upper() else True

    def getAlertLabels(self,h):
        return [el.text.strip() for el in h.find_elements_by_tag_name("label")]

    def getThresholdIconColor(self,h):
        return h.find_element_by_tag_name("circle").get_attribute("fill").strip()

    def getAlertFullBody(self,h,parent,child):

        pass

    def getAlertHeader(self,h):
        pass


