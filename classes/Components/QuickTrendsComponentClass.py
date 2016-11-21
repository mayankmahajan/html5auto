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

from selenium.webdriver import ActionChains



class QuickTrendsComponentClass(BaseComponentClass):
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

    def moveTotick(self,driverHelper,handlrs):
        h = self.__getHandler(handlrs)
        hxaxis = self.__getHandleAxis(h['chart'], 'wm-axis')
        for el in hxaxis:
            if el.tag_name == 'g':
                hticks = self.__getHandleTicks(el, 'tick')
                tooltipText=[]
                for el in hticks:
                    driverHelper.action.move_to_element(el).perform()
                    tooltipText.append(handlrs['qttooltip'][len(handlrs['qttooltip'])-1].text)
            else:
                print el.tag_name
        return tooltipText



    def __getHandler(self, handlrs):
        h = {}
        for svg in handlrs['quicktrends'][0].find_elements_by_tag_name("svg"):
            if len(svg.find_elements_by_class_name('legend')) > 0:
                h['legend']= svg
            else:
                h['chart']= svg
             # if len(svg.find_elements_by_class_name('legend')) > 0 else
        return h

    def getLegendList(self,handlrs):
        h = self.__getHandler(handlrs)
        return (h['legend'].text).split('\n')






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
