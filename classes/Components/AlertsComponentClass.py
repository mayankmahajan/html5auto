from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *

class AlertsComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getAlertList(self,h,parent,child):
        list = []
        for row in h[parent][child]:
            list.append(self.createAlertListObject(row))
            # list[temp['header']+"$$"+temp['duration']] = temp
        return list


    def selectAlert(self,index,h,parent='alertlist',child="list"):
        try:
            h[parent][child][index].click()
            return True
        except:
            return False


    def getSelectedAlert(self,h,parent,child):
        return self.getAlertList(h,parent,child)

    def createAlertListObject(self,h):
        alertObject={}
        alertObject['state'] = self.getAlertHandledIcon(h)
        alertObject['header'] = self.getAlertLabels(h)[0]
        alertObject['duration'] = self.getAlertLabels(h)[1]
        alertObject['alarmcount'] = self.getAlertLabels(h)[2]
        alertObject['measure'] = self.getAlertLabels(h)[3]
        alertObject['color'] = self.getThresholdIconColor(h)
        return alertObject

    def getAlertHandledIcon(self,h):
        return False if "UnHandled".upper() in h.find_element_by_tag_name("img").get_attribute("class").upper() else True

    def getAlertLabels(self,h):
        return [el.text.strip() for el in h.find_elements_by_tag_name("label")]

    def getThresholdIconColor(self,h):
        return h.find_element_by_tag_name("circle").get_attribute("fill").strip()

    def getAlertFullBody(self,h,parent="alertinfo",child=""):
        alertBOdyObject = self.createAlertBodyObject(h[parent])

        pass

    def createAlertBodyObject(self,h):

        alertBOdyObject = {}
        alertBOdyObject['state'] =  False if "UnHandled".upper() in h['state'][0].text.upper() else True
        alertBOdyObject['header'] = self.getAlertHeader(h)
        alertBOdyObject['range'],alertBOdyObject['alarmcount'] = self.getAlertDuration(h)
        alertBOdyObject['alarmrows'] = self.getAlarmRows(h)
        alertBOdyObject['ruleName'], alertBOdyObject['gran'], alertBOdyObject['type'] = self.getRuleInfo(h)


        alertBOdyObject['measure'] = self.getAlertHandledIcon(h)
        alertBOdyObject['color'] = self.getAlertHandledIcon(h)


        alertBOdyObject['links'] = h['links']
        alertBOdyObject['alerttable'] = h['alerttable']


    def getAlarmRows(self,h):
        alarmsrows = []
        for el in h['alarm-row']:
            alarmsrows.append(el.text)
        return alarmsrows

    def getAlertHeader(self,h,child="header"):
        return h[child][0].text

    def getAlertDuration(self,h,child="timecount"):
        time = h[child][0].find_elements_by_class_name("time")[0].text
        count = h[child][0].find_elements_by_class_name("count")[0].text
        return time,count

    def getRuleInfo(self,h,child=""):
        handleTosiblings = self.getAllRuleSiblings(h)
        siblings = []
        for el in handleTosiblings:
            siblings.append(el.text)
        return siblings[2],siblings[4],siblings[6]

    def getAllRuleSiblings(self,h,child="alertinfo"):
        for el in h[child][0].find_elements_by_tag_name("span"):
            if el.text == "Rule":
                return el.find_elements_by_xpath("..//span")


    #def getAlertHeader(self,h):
     #   pass


