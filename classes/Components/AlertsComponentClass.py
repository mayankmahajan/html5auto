from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *
from classes.Components.SearchComponentClass import *
from classes.Components.DropdownComponentClass import *
from Utils.UnitSystem import *

class AlertsComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()
        self.search=SearchComponentClass()
        self.dropdown = DropdownComponentClass()
        self.colors = self.configmanager.getNodeElements("colors","color")
        self.unitSystem = UnitSystem()


    def getAlertList(self,h,parent,child):
        list = []
        for row in h[parent][child]:
            list.append(self.createAlertListObject(row))
            # list[temp['header']+"$$"+temp['duration']] = temp
        return list


    def selectAlert(self,index,h,parent='alertlist',child="list"):
        try:
            h[parent][child][index].click()
            return self.getAlertList(h,parent,"selected")
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
        alertObject['event'] = alertObject['measure']+" - crossed "+alertObject['color'] +" Threshold"
        return alertObject

    def getAlertHandledIcon(self,h):
        return False if "UnHandled".upper() in h.find_element_by_tag_name("img").get_attribute("class").upper() else True

    def getAlertLabels(self,h):
        return [el.text.strip() for el in h.find_elements_by_tag_name("label")]

    def getThresholdIconColor(self,h):
        return self.getColorName(h.find_element_by_tag_name("circle").get_attribute("fill").strip())

    def getAlertFullBody(self,h,parent="alertinfo",child=""):
        alertBOdyObject = self.createAlertBodyObject(h[parent])

        return alertBOdyObject

    def createAlertBodyObject(self,h):

        alertBOdyObject = {}
        alertBOdyObject['state'] =  False if "UnHandled".upper() in h['state'][0].text.upper() else True
        alertBOdyObject['header'] = self.getAlertHeader(h)
        alertBOdyObject['range'],alertBOdyObject['alarmcount'] = self.getAlertDuration(h)
        alertBOdyObject['alarmrows'] = self.getAlarmRows(h)
        alertBOdyObject['ruleName'], alertBOdyObject['gran'], alertBOdyObject['type'] = self.getRuleInfo(h)


        alertBOdyObject['measure'] =  h['alerttable'][2].find_elements_by_xpath(".//td")[0].text
        alertBOdyObject['filters'] = self.getFormattedFilters(h)
        alertBOdyObject['color'] = self.getColor(h)
        alertBOdyObject['event'] = ""
        for el in self.getAllSiblings(h,alertBOdyObject['measure'],"span","alertinfo"):
            alertBOdyObject['event'] = alertBOdyObject['event']+el.text

        # alertBOdyObject['event'] = self.getAllSiblings(h,alertBOdyObject['measure'],"span","alertinfo")
        #

        # alertBOdyObject['links'] = h['links']
        alertBOdyObject['conditions'] = self.createConditions(h)

        return alertBOdyObject

    def getColor(self,h,child='color'):
        color = h[child][0].get_attribute('style').strip(";").split('rgb')[1]
        for el in h[child]:
           if color !=el.get_attribute('style').strip(";").split('rgb')[1]:
               return False
        return self.getColorName(self.rgb_to_hex(color))

    def createConditions(self,h,child="alerttable"):
        arr = ["-","-","-"]

        condition = h[child][2].find_elements_by_xpath(".//td")[1].text.replace(" ","")
        if "critical" in h[child][2].find_elements_by_xpath(".//td")[2].text.lower():
            arr[2] = condition
        elif "minor" in h[child][2].find_elements_by_xpath(".//td")[2].text.lower():
            arr[0] = condition
        elif "major" in h[child][2].find_elements_by_xpath(".//td")[2].text.lower():
                arr[1] = condition
        return arr


    def getFormattedFilters(self,h,child="alerttable"):
        tds = h[child][1].find_elements_by_xpath(".//td")
        filters = ''
        for i in range(0,len(tds),2):
            filters=filters+tds[i].text+":"+tds[i+1].text+","
        return filters.strip(",")


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
        handleTosiblings = self.getAllSiblings(h,"Rule","span","alertinfo")
        siblings = []
        for el in handleTosiblings:
            siblings.append(el.text)
        return siblings[2],siblings[4],siblings[6]

    # def getAllSiblings(self, h, text="Rule", tag="span", child="alertinfo"):
    #     tagpath = "..//"+tag
    #     for el in h[child][0].find_elements_by_tag_name(tag):
    #         if el.text == text:
    #             return el.find_elements_by_xpath(tagpath)


    #def getAlertHeader(self,h):
     #   pass

    def rgb_to_hex(self,rgb):
        if 'rgba' not in rgb:
            x = rgb.strip('\(').strip('\)').split(',')
        else:
            # ignoring alpha property
            x= rgb.split('rgba')[1].strip('\(').strip('\)').split(',')

        rgb = (int(x[0]),int(x[1]),int(x[2]))
        return '#%02x%02x%02x' % rgb

    def getSeverityWiseCount(self,alertList):
        calculatedcount = {}
        calculatedcount['total'] = 0
        for el in alertList:
            if el['color'] in calculatedcount:
                calculatedcount[el['color']]= calculatedcount[el['color']] +int(el['alarmcount'].split()[0])
                calculatedcount['total'] = calculatedcount['total'] +int(el['alarmcount'].split()[0])
            else:
                calculatedcount[el['color']]= 0
                calculatedcount[el['color']]= calculatedcount[el['color']] +int(el['alarmcount'].split()[0])
                calculatedcount['total'] = calculatedcount['total']+int(el['alarmcount'].split()[0])

        return calculatedcount

    def getAlertsFromCounterBar(self,h):
        d={}
        try:
            d['total'] = int(h['total'][0].text.split()[0])
        except ValueError as e:
            d['total'] = int(self.unitSystem.getRawValue(float(h['total'][0].text.split()[0]),str(h['total'][0].text.split()[1])))
        except Exception as e:
            return e


        text = h['severity'][0].text
        def _getUIValue(text):
            splits = text.split()
            if len(splits)>1:
                return float(splits[0]),str(splits[1])
            else:
                return float(splits[0]),""



        # d[self.getColorName(self.rgb_to_hex(h['colors'][0].value_of_css_property("background-color")))] =\
        #     int(self.unitSystem.getRawValue(float(h['severity'][0].text.split()[0]),str(h['severity'][0].text.split()[1])))
        # d[self.getColorName(self.rgb_to_hex(h['colors'][1].value_of_css_property("background-color")))] =\
        #     int(self.unitSystem.getRawValue(float(h['severity'][1].text.split()[0]),str(h['severity'][1].text.split()[1])))
        # d[self.getColorName(self.rgb_to_hex(h['colors'][2].value_of_css_property("background-color")))] =\
        #     int(self.unitSystem.getRawValue(float(h['severity'][2].text.split()[0]),str(h['severity'][2].text.split()[1])))

        d[self.getColorName(self.rgb_to_hex(h['colors'][0].value_of_css_property("background-color")))] =\
            int(self.unitSystem.getRawValue(*_getUIValue(h['severity'][0].text)))
        d[self.getColorName(self.rgb_to_hex(h['colors'][1].value_of_css_property("background-color")))] =\
            int(self.unitSystem.getRawValue(*_getUIValue(h['severity'][1].text)))
        d[self.getColorName(self.rgb_to_hex(h['colors'][2].value_of_css_property("background-color")))] =\
            int(self.unitSystem.getRawValue(*_getUIValue(h['severity'][2].text)))


        return d

    def getTotalAlerts(self,alertList,h,parent="counter",child=""):
        count = self.getAlertsFromCounterBar(h[parent])
        calculatedcount = self.getSeverityWiseCount(alertList)
        logger.info("Got Counters from Bar  = %s",str(count))
        logger.info("Got Calculated Counts from Alert Lists  = %s",str(calculatedcount))
        return count,calculatedcount

    def getColorName(self,col):
        for color in self.colors:
            if col in color or str(col).lower() in color:
                return str(color).split('#')[0]
        return str(col)


# http://stackoverflow.com/questions/37090653/iterating-through-table-rows-in-selenium-python
# from lxml import html
# xml = html.fromstring(h)
# # gets the table
# table =  xml.xpath("//table[@class='datadisplaytable']")[0]
#
#
# # iterate over all the rows
# for row in table.xpath(".//tr"):
#      # get the text from all the td's from each row
#     print([td.text for td in row.xpath(".//td[@class='dddefault'][text()])