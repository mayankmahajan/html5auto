#!/usr/bin/env python
##############################################################
'''
FPV Component Handler
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
import re
from Utils.logger import *


from selenium.webdriver import ActionChains



class FPVComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getData(self,h,parent="fpv",child="container"):
        handler=h[parent][child]
        rankHandlers = self.getRanks(handler[0],"class","rankClass")
        totalPaths = len(rankHandlers)/2
        hopsArray = self.getHops(handler[0])
        circularAreas = self.getclickableCircularArea(handler[0],"class","rankClass")

        paths = []
        for el in circularAreas:
            try:
                logger.debug('Clicking Element :: Parent %s Child %s Object %s',parent,child,el.text)
                el.click()
            except Exception as e:
                logger.debug('Exception %s found on clicking Parent %s Child %s Object %s',e,parent,child,el.text)
                return e

            lineArray = self.getConnectingLines(handler[0])
            paths.append(self.createUniquePaths(totalPaths,hopsArray,lineArray))

        return [self.dataPerPath(rankHandlers),self.arrangeHops(paths,hopsArray)]

    def dataPerPath(self,rankHandlers):
        return [rankHandlers[i].text for i in range(len(rankHandlers)/2)]

    def arrangeHops(self,paths,hopsArray):
        arrangedPaths = {}
        for i in range(len(paths)):
            arrangedPaths[str(i)]=""
            for j in range(len(hopsArray)):
                for el in hopsArray[j]:
                    if el+"_C"+str(j+1) in paths[i]:
                        arrangedPaths[str(i)]=arrangedPaths[str(i)]+el+"_"
        return arrangedPaths



        pass





    def createUniquePaths(self,totalPaths,hopsArray,lineArray):
        coloredPaths = [el.get_attribute("style")+"$$"+el.get_attribute("id") for el in lineArray[0]]
        # coloredPaths = [[el.get_attribute("style"),el.get_attribute("id")] for el in lineArray[0]]
        colors = self.getUniqueColors(coloredPaths)
        selectionColor = self.getSelectionColor(colors,coloredPaths)
        return self.createPath(selectionColor,coloredPaths)


    def createPath(self,selectionColor,coloredPaths):
        path = ""
        for el in coloredPaths:
            if selectionColor in el:
                path = path + el.split("$$")[1] + "_"
        return path



    def getSelectionColor(self,colors,coloredPaths):
        temp = [el for el in sorted(coloredPaths) if "#" in el]
        f = 0
        for color in colors:
            for el in temp:
                if color in el:
                    f = f + 1
            if f == 1:
                return color
            f = 0





    def getSelectedPath(self,colors,paths):
        # colors = self.getUniqueColors(paths)
        x =[]
        for el in colors:
            for e in paths:
                x.append()


        for el in paths:
            colors

    def getUniqueColors(self,paths):
        colors= []
        colors.append(paths[0].split("$$")[0])
        for el in paths:
            if el.split("$$")[0] not in colors:
                colors.append(el.split("$$")[0])

        return colors





    def createUniquePaths1(self,totalPaths,hopsArray,lineArray):

        pathStarts = [el for el in lineArray[1] if "#" in el]
        for el in pathStarts:
            connection0 = re.compile(r'\#[0-9]_+').split(el)[1]
            self.findNextLinks(lineArray[1],connection0,len(hopsArray))
            # connection1 = re.compile(r'\_C').split(re.compile(r'\#[0-9]_+').split(el)[1])[0]


        pass

    def findNextLinks(self,lines,connection,totalHops):
        connections=[]
        for i in range(totalHops):
            connections.append([e for e in lines if connection in e and "#" not in e])
            connection = ""
            # regExp = "r'\_C"+str(i+1)+"_'"
            regExp = "_C"+str(i+1)+"_"
            for el in connections:
                connection = re.compile(regExp).split(connections[i])



        if connection in lines:
            pass



    def getRanks(self,h,prop,value):
        if prop == "class":
            return self.getAllActiveElements(h.find_element_by_class_name(value).find_elements_by_tag_name("text"))
        elif prop == "id":
            return self.getAllActiveElements(h.find_elements_by_id(value).find_elements_by_tag_name("text"))

    def getclickableCircularArea(self,h,prop,value):
        if prop == "class":
            return self.getAllActiveElements(h.find_element_by_class_name(value).find_elements_by_tag_name("circle"))


    def getHops(self,h):
        hopsHandler = self.getAllActiveElements(h.find_elements_by_class_name("hopClass"))
        hops = []
        arr = []
        for el in hopsHandler:
            # arr = []
            visiblechilds = self.getAllActiveElements(el.find_elements_by_xpath(".//*"))
            # arr.append([el.get_attribute("id") for el in visiblechilds if el.tag_name == "rect"])
            arr.append([el.text for el in visiblechilds if el.tag_name == "text"])
            # hops.append(arr)
        # return hops
        return arr

    def getConnectingLines(self,h):
        # linesHandler = self.getAllActiveElements([el for el in h.find_elements_by_tag_name("line") if "_C" in el.get_attribute("id") ])
        linesHandler = [el for el in h.find_elements_by_tag_name("line") if "_C" in el.get_attribute("id") and "up" not in el.get_attribute("id") and "down" not in el.get_attribute("id")]
        return [linesHandler,[el.get_attribute("id") for el in linesHandler]]


