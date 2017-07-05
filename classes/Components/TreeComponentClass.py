# coding=utf-8
from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
import time
from Utils.logger import *
from selenium.webdriver.common.keys import *
from selenium.webdriver import ActionChains
from MRXUtils.MRXConstants import *
import random


class TreeComponentClass(BaseComponentClass):


    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.utility = __import__("Utils.utility")
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

    def expandTree(self,treeHandle,parent='alltrees',child='tree',index=0):
        logger.info('Going to expand Tree')
        return self.expandTree1(treeHandle[parent][child][index])

    def expandTree1(self,treeElementHandle):
        tree_nodes=treeElementHandle.find_elements_by_tag_name('treenode')
        if len(tree_nodes)>5:
            l = [tree_nodes[random.randrange(len(tree_nodes))] for item in range(MRXConstants.NumberOfElementToBeExpandOnAtAnyLevel)]
            treenodes = list(set(l))
        else:
            treenodes = tree_nodes
        for ele in treenodes:
            if 'leaf' in ele.find_elements_by_xpath('./*')[0].get_attribute('class'):
                continue
            else:
                ele.find_elements_by_class_name('toggle-children')[0].click()
                self.expandTree1(ele)


    def expandTree1_old(self,treeElementHandle):
        for ele in treeElementHandle.find_elements_by_tag_name('treenode'):
            if 'leaf' in ele.find_elements_by_xpath('./*')[0].get_attribute('class'):
                continue
            else:
                ele.find_elements_by_class_name('toggle-children')[0].click()
                self.expandTree1(ele)


    def doSelectionOnTree_Random(self,setup,elementDict,treeHandle,parent='alltrees',child='tree',index=0):
        elementToBeSelect={}
        for k in elementDict.keys():
            if len(elementDict[k])>MRXConstants.NumberOfSelectionOnAtAnyLevel:
                l=[elementDict[k][random.randrange(len(elementDict[k]))] for item in range(MRXConstants.NumberOfSelectionOnAtAnyLevel)]
                elementToBeSelect[k]=list(set(l))
            else:
                elementToBeSelect[k]=elementDict[k]

        expectedTextFormUIForSelectedTree=[]
        # for k in elementToBeSelect.keys():
        #     expectedText=self.selectTree(setup,treeHandle,elementToBeSelect[k],index=index)
        #     expectedTextFormUIForSelectedTree.append(expectedText)

        expected={}
        for k in elementToBeSelect.keys():
            expected[k]=self.selectTree(setup,treeHandle,elementToBeSelect[k],index=index)

        keysList=expected.keys()  ### for verify level 1>2>3...###
        keysList.sort()
        for k in keysList:
            expectedTextFormUIForSelectedTree.append(expected[k])

        return str(' > '.join(expectedTextFormUIForSelectedTree)),elementToBeSelect,self.getSelectionFromExpendedTree(treeHandle,index=index)


    def getSelectionFromExpendedTree(self,treeHandle,parent='alltrees',child='tree',index=0):
        selectedElements = {}
        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('treenodecontent'):
            key = str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip()
            if not key in selectedElements.keys():
                selectedElements[key] = []

        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('treenodecontent'):
            if 'active' in ele.find_elements_by_xpath('../../../div')[0].get_attribute('class'):
                selectedElements[str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip()].append(str(ele.text).strip())
        return selectedElements



    def selectTree(self,setup,treeHandle,listForSelection,parent='alltrees',child='tree',index=0):
        List = []
        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('treenodecontent'):
            try:
                if str(ele.text).strip() in listForSelection:
                    try:
                        logger.info('Going to select %s on tree',str(ele.text))
                        ActionChains(setup.d).key_down(Keys.SHIFT).perform()
                        ele.click()
                        List.append(str(ele.text))
                        ActionChains(setup.d).key_down(Keys.SHIFT).perform()
                    except Exception as e:
                        logger.error('Got exception during selection on Tree:: Exception = %s',str(e))
            except:
                #uncode char handling
                pass
        return '( '+str(', '.join(List))+')'


    def seprateElementOfTreeByLevel(self,treeHandle,parent='alltrees',child='tree',index=0):
        classname = []
        element_list = []
        for ele in treeHandle[parent][child][index].find_elements_by_tag_name('treenodecontent'):
            try:
                element_list.append(str(ele.text).strip())
                classname.append(str(ele.find_elements_by_xpath('../../../div')[0].get_attribute('class').split(' ')[1]).strip())
            except:
                # uncode char handling
                pass

        level_Dict = {}
        for level in classname:
            if not level in level_Dict.keys():
                level_Dict[level] = []

        for i in range(len(element_list)):
            level_Dict[classname[i]].append(element_list[i])
        return level_Dict

