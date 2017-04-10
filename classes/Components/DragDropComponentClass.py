#!/usr/bin/env python
##############################################################
'''
BarTabular Component Handler
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



class DragDropComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()

        with open("/Users/mayank.mahajan/PycharmProjects/html5automation/classes/DriverHelpers/drag_and_drop_helper.js","r") as f:
            self.java_script = f.read()
            self.method = ".simulateDragDrop"

    # driver.execute_script('arguments[0].setAttribute(arguments[1],arguments[2])',selecteds[0],"id","hahah")

    def set_attribute(self,setup,elem,property,value):
        setAtr = 'arguments[0].setAttribute(arguments[1],arguments[2])'
        setup.d.execute_script(setAtr,elem,property,value)

    def dragDrop(self,setup,source,target):
        # selectedRows = setup.d.execute_script('return $(".selectedRowClass")')
        src='$("#'+source+'")'
        trg = '({"dropTarget":"#'+target+'"});'
        setup.d.execute_script(self.java_script)
        time.sleep(8)
        print src+self.method+trg
        setup.d.execute_script(src+self.method+trg)

        # setup.d.execute_script(self.java_script+'$("#drag2").simulateDragDrop({"dropTarget":"#drop1"});')

