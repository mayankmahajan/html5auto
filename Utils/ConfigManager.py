#!/usr/bin/env python
##############################################################
'''
Manages configs
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
from xml.etree.ElementTree import TreeBuilder
from xml.etree.ElementTree import ElementTree
import glob

from Utils.XMLCombiner import XMLCombiner


class ConfigManager(object):
    __instance = None

    def __init__(self):
        # self.tree = self.mergeScreenConfigs()
        # self.tree = self.parse()
        self.tree = XMLCombiner(['/Users/mayank.mahajan/PycharmProjects/html5automation/configs/coreconfig.xml', '/Users/mayank.mahajan/PycharmProjects/html5automation/configs/solutionconfig.xml']).combine()

        self.root = self.tree.getroot()
        self.screenComponentRelations = self.getScreenComponentRelations()
        self.componentChildRelations = self.getComponentChildRelations()
        self.screenSelectors = self.getScreenConfigs()
        self.componentSelectors = self.getComponentSelectors()

    def __new__(cls):
        if ConfigManager.__instance is None:
            ConfigManager.__instance = object.__new__(cls)
        # ConfigManager.__instance.val = val
        return ConfigManager.__instance

    def getScreenConfigs(self):
        screenConfigs = self.tree.getiterator('screenConfig')
        # screenConfigDetails = []
        tempDict = {}
        for child in screenConfigs:
            # tempArray = []
            # tempDict = {}
            tempDict[child.attrib['id']] = {}

            childComponents = child.findall('component')
            for component in childComponents:
                # tempDict[child.attrib['id']]
                tempDict[child.attrib['id']][component.attrib['id']] = {}
                tempDict[child.attrib['id']][component.attrib['id']] = component.attrib
                # screenConfigDetails.append(tempDict)
        return tempDict

    def getComponentConfigs(self):
        screenConfigs = self.tree.getiterator('componentConfig')
        # screenConfigDetails = []
        tempDict = {}
        for child in screenConfigs:
            # tempArray = []
            # tempDict = {}
            tempDict[child.attrib['id']] = {}

            childComponents = child.findall('component')
            for component in childComponents:
                # tempDict[child.attrib['id']]
                tempDict[child.attrib['id']][component.attrib['id']] = {}
                tempDict[child.attrib['id']][component.attrib['id']] = component.attrib
                # screenConfigDetails.append(tempDict)
        return tempDict


    def getComponentConfigsPerScreen(self,screenID):
        componentsInScreen = {}
        componentsInScreen = self.getComponentListFromScreenConfigs(screenID)
        keys = []
        for key,value in componentsInScreen.iteritems():
            keys.append(key)
        # return keys
        return self.getComponentConfigsFromIds(keys)

    def getScreenComponentRelations(self,screenID=""):
        screenConfigs = self.getScreenConfigs()
        list = {}
        for key,value in screenConfigs.iteritems():
            l = []
            for k,v in screenConfigs[key].iteritems():
                l.append(k)
            list[key] = l
        if screenID != "":
            try:
                return list[screenID]
            except ValueError:
                return ValueError
        else:
            return list

    def getComponentChildRelations(self,componentID=""):
        compConfigs = self.getComponentConfigs()
        list = {}
        for key,value in compConfigs.iteritems():
            l = []
            for k,v in compConfigs[key].iteritems():
                l.append(k)
            list[key] = l
        if componentID != "":
            try:
                return list[componentID]
            except ValueError:
                return ValueError
        else:
            return list
    def getComponentSelectors(self,componentID=""):
        compConfigs = self.getComponentConfigs()
        list = {}
        for key,value in compConfigs.iteritems():
            for k,v in compConfigs[key].iteritems():
                list[k] = v
        if componentID != "":
            try:
                return list[componentID]
            except ValueError:
                return ValueError
        else:
            return list

    def getSelectionParams(self,componentID):
        self.selectionList = {}
        return True

    def getComponentListFromScreenConfigs(self,screenID):
        screenConfigs = self.getScreenConfigs()
        for key,value in screenConfigs.iteritems():
            if key == screenID:
                return screenConfigs[key]

    def getComponentConfigsFromIds(self,compArray):
        componentConfigs = self.getComponentConfigs()
        listOfRelevantConfigs = {}
        for key,value in componentConfigs.iteritems():
            if key in compArray:
                listOfRelevantConfigs[key]=value
        return listOfRelevantConfigs









    # def mergeScreenConfigs(self):
    #     xml_files = ["../configs/coreconfig.xml","../configs/solutionconfig.xml"]
    #     xml_element_tree = None
    #     for xml_file in xml_files:
    #         data = ET.parse(xml_file).getroot()
    #         # print ElementTree.tostring(data)
    #         for result in data.iter('screenConfigs'):
    #             if xml_element_tree is None:
    #                 xml_element_tree = data
    #                 insertion_point = xml_element_tree.findall("./screenConfigs")[0]
    #             else:
    #                 insertion_point.extend(result)
    #     if xml_element_tree is not None:
    #         print ET.tostring(xml_element_tree)
    #         return ET.tostring(xml_element_tree)
            # return xml_element_tree
        # return xml_element_tree

        #
        #
        #
        # solTree = ET.parse('../configs/solutionconfig.xml')
        # coreTree = ET.parse('../configs/coreconfig.xml')
        #
        # mergedTree = []     #tree with all the nodes present in solution and core configs
        # return mergedTree

    def parse(self, source=None, parser=None):
        try:
            if not parser:
                parser = XMLParser(target=TreeBuilder())
            while 1:
                data = self.mergeScreenConfigs()
                if not data:
                    break
                parser.feed(data)
            return parser.close()
            # self._root = parser.close()
            # return self._root
        except:
            pass
