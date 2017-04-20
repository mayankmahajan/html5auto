#!/usr/bin/env python
##############################################################
'''
Quick Trends Component Handler
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################



from BaseComponentClass import BaseComponentClass
from classes.DriverHelpers.locators import *
from Utils.Constants import *
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *

from selenium.webdriver import ActionChains



class QuickTrendsComponentClass(BaseComponentClass):
    def __init__(self):
        self.util = __import__("Utils.utility")
    # 'Yes' if fruit == 'Apple' else 'No'

    # parentHandles['quicktrends'][0].find_elements_by_tag_name("svg")[0].find_elements_by_class_name('legend')

    def __getHandleAxis(self, hChart, xy):
        return hChart.find_elements_by_class_name(xy)

    def __getHandleTicks(self, hChartxy, tick):
        return hChartxy.find_elements_by_class_name(tick)

    def __getAxisTicks(self, h, xy):
        axis = {}
        for ele in self.__getHandleAxis(h['chart'], xy):
            if ele.tag_name == 'g':
                axis['ticks'] = [e.text for e in self.__getHandleTicks(ele, 'tick')]
            else:
                axis['xtitle'] = ele.text
        return axis

    def getXAxis(self,handlrs):
        h = self.__getHandler(handlrs)
        xaxis = self.__getAxisTicks(h, "wm-axis")
        return xaxis

    def getYAxis(self,handlrs):
        h = self.__getHandler(handlrs)
        yaxis = self.__getAxisTicks(h, "wm-yaxis")
        return yaxis

    def moveTotick(self,driverHelper,handlrs,setup):
        h = self.__getHandler(handlrs)
        hxaxis = self.__getHandleAxis(h['chart'], 'wm-axis')
        for el in hxaxis:
            if el.tag_name == 'g':
                hticks = self.__getHandleTicks(el, 'tick')
                tooltipText=[]
                for el in hticks:
                    driverHelper.action.move_to_element(el).perform()
                    tempHandlers = self.util.utility.getHandle(setup,"qt_Screen","quicktrends")
                    # time.sleep(1) # only to show in demo
                    tooltipText.append(tempHandlers['quicktrends']['qttooltip'][len(tempHandlers['quicktrends']['qttooltip'])-1].text)
            else:
                print el.tag_name
        return tooltipText

    def hoverOverTicksGetMainChartText(self, setup, h1, screenName, parent="trend-main", child="trendchart", parent_tooltip="trend-header", child_tooltip="qttooltip"):
        try:
            h = self.__getHandler1(h1[parent][child])
            hxaxis = self.__getHandleAxis(h['chart'], 'wm-axis')
            for el in hxaxis:
                if el.tag_name == 'g':
                    hticks = self.__getHandleTicks(el, 'tick')
                    tooltipText={}
                    for el in hticks:
                        logger.info("Going to perform Hover Action")
                        setup.dH.action.move_to_element(el).perform()
                        logger.info("Hover Action Performed")
                        tempHandlers = self.util.utility.getHandle(setup,screenName,parent)
                        time.sleep(1) # only to show in demo
                        headerhandles = self.util.utility.getHandle(setup,screenName,parent_tooltip)
                        time.sleep(1) # only to show in demo
                        tooltipText[str(tempHandlers[parent][child_tooltip][0].text)] = str(headerhandles[parent_tooltip][child_tooltip][0].text)
                else:
                    print el.tag_name
            logger.debug("Got tooltip data =  %s",str(tooltipText))
            return tooltipText
        except Exception as e:
            logger.error("Got Exception while performing hover actions = %s",str(e))
            return e

    def hoverOverTicksGetMainAndCompareChartText(self, setup, h1, screenName, parent="trend-main", child="trendchart",compare_parent = "trend-compare",active_compare_chart = 0, parent_tooltip="trend-header", child_tooltip="qttooltip"):
        try:
            h = self.__getHandler1(h1[parent][child])
            hxaxis = self.__getHandleAxis(h['chart'], 'wm-axis')
            for el in hxaxis:
                if el.tag_name == 'g':
                    hticks = self.__getHandleTicks(el, 'tick')
                    tooltipText={}
                    compareTooltipText={}
                    for el in hticks:
                        logger.info("Going to perform Hover Action")
                        setup.dH.action.move_to_element(el).perform()
                        logger.info("Hover Action Performed")
                        tempHandlers = self.util.utility.getHandle(setup,screenName,parent)
                        time.sleep(1) # only to show in demo

                        compareHandlers = self.util.utility.getHandle(setup,screenName,compare_parent)
                        time.sleep(1) # only to show in demo

                        headerhandles = self.util.utility.getHandle(setup,screenName,parent_tooltip)
                        time.sleep(1) # only to show in demo

                        tooltipText[str(tempHandlers[parent][child_tooltip][0].text)] = str(headerhandles[parent_tooltip][child_tooltip][0].text)

                        compareTooltipText[str(tempHandlers[parent][child_tooltip][0].text)] = str(compareHandlers[compare_parent][child_tooltip][active_compare_chart].text)
                else:
                    print el.tag_name
            logger.debug("Got tooltip data from main Chart =  %s and from compare chart = %s",str(tooltipText),str(compareTooltipText))
            return tooltipText,compareTooltipText
        except Exception as e:
            logger.error("Got Exception while performing hover actions = %s",str(e))
            return e


    def getHoverText(self, h,parent="trend-header", child="qttooltip",index=0):
        return str(h[parent][child][index].text).strip()
        # return str(h[parent_tooltip][child][0].text),str(h[parent][child_tooltip][0].text)

    # def getHoverTextFromCompareChart(self, h,parent="trend-compare", child="qttooltip",index=0):
    #     return  str(h[parent][child][index].text).strip()



    def getDimensionFromCompareChart(self,h,index=0,parent="trend-compare",child="comparedimension",removeChar="By"):
        try:
            logger.info("Getting Dimension Selected on CompareChart %d",index)
            dim = str(h[parent][child][index].text).strip().strip('\n').strip().split(removeChar)[1].strip()
            logger.info("Got Dimension Selected on CompareChart %d = %s",index,dim)
            return dim
        except Exception as e:
            logger.error("Got Exception while Getting Dimension Selected on CompareChart %d = %s",index,str(e))
            return e







    def __getHandler(self, handlrs):
        h = {}
        for svg in handlrs['quicktrends']['quicktrends'][0].find_elements_by_tag_name("svg"):
            if len(svg.find_elements_by_class_name('legend')) > 0:
                h['legend']= svg
            else:
                h['chart']= svg
             # if len(svg.find_elements_by_class_name('legend')) > 0 else
        return h

    def __getHandler1(self, handlrs):
        h = {}
        for svg in self.getAllActiveElements(handlrs[0].find_elements_by_tag_name("svg")):
            if len(svg.find_elements_by_class_name('legend')) > 0:
                h['legend']= svg
            else:
                h['chart']= svg
             # if len(svg.find_elements_by_class_name('legend')) > 0 else
        return h



    def getLegendList(self,handlrs):
        h = self.__getHandler(handlrs)
        return (h['legend'].text).split('\n')

    def getLegends_tm(self,h,parent="trend-legend",child="legend"):
        try:
            legends = []
            for legend in h[parent][child]:
                temp = {}
                temp['color'] = self.rgb_to_hex(legend.find_elements_by_xpath("./div[1]")[0].value_of_css_property("background-color"))
                temp['state'] = not legend.find_elements_by_xpath("./div[1]/img")[0].is_displayed()
                temp['value'] = legend.find_elements_by_xpath("./div[2]")[0].text
                temp['handle'] = legend
                legends.append(temp)
            return legends
        except Exception as e:
            return e


    def clickLegendByIndex_tm(self,index, h,parent="trend-legend",child="legend"):

        legends = self.getAllActiveElements(h[parent][child])
        logger.info("Got total legends = %d",len(legends))

        for i in range(len(legends)):
            if i == index:
                try:
                    color = self.rgb_to_hex(legends[i].find_elements_by_xpath("./div[1]")[0].value_of_css_property("background-color"))
                    value = legends[i].find_elements_by_xpath("./div[2]")[0].text
                    legends[i].find_elements_by_xpath("./div[1]")[0].click()
                    logger.info("Legend clicked = %s with name = %s",str(color),str(value))
                    return color
                except Exception as e:
                    return e
        return False

    def getPaths(self,h,parent="trend-main", child="trendchart",indexOfComp=0):
        paths = []
        # for el in h[parent][child][indexOfComp].find_elements_by_tag_name("path"):img[contains(@id, "tartTime")]
        for el in h[parent][child][indexOfComp].find_elements_by_css_selector("g.series path"):
            paths.append(self.rgb_to_hex(el.get_attribute("stroke")))
        return paths

    def getChartsCount(self, h, parent="trend-main", child="trendchart"):
        return len(h[parent][child])

    def getSelectedCompareChartIndex(self, h, parent="trend-compare", child="trendchart",selectedColor="#ffffff"):
        childs = h[parent][child]
        for index in range(len(childs)):
            color = self.rgb_to_hex(childs[index].find_elements_by_xpath("../../div[1]")[0].value_of_css_property("background-color"))
            if color == selectedColor:
                return index
        return False




    def clickOnExpandButton(self,h,parent="trend-slider",child='expand-btn'):
        if len(h[parent][child]) > 0:
            h[parent][child][0].click()
            try:
                h[parent][child][0].click()
            except:
                pass






                # def getTooltipInfo(self,handlrs):
    #     h = self.getHandler(handlrs)




    # def getLineSeriesHandles(self,h):
    #     h1 = self.getHandler(h)
    #     h1['chart'].find_elements_by_class_name("series")





    # def getLegendHandler(self,handlrs):
    #     return handlrs['quicktrends'][0].find_elements_by_tag_name("svg")[0].find_elements_by_class_name('legend')[0]
    #
    # def getChartHandler(self,handlrs):
    #     return handlrs['quicktrends'][0].find_elements_by_tag_name("svg")[0].find_elements_by_class_name('legend')[0]

    # def parseChart(self,handlrs):
    #     pass
