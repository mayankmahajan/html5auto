#!/usr/bin/env python
##############################################################
'''
Called Directly from TestCase
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################


from Utils.utility import *
from classes.Pages.GenerateReportsPopClass import GenerateReportsPopClass
from MuralConstants import *


def createAlert(setup):

    pass

def setName(name,handle):
    instance = DropdownComponentClass()
    return instance.sendkeys_input(name,handle,0)

def setDrop(value,index,handle):
    instance = DropdownComponentClass()
    return instance.doSelectionOnVisibleDropDown(handle,value,index)

def setCondition(priorty, operator, number_value, unitSystem, handle, setup):
    if priorty==0:
        index = 3
    elif priorty==1:
        index = 5
    elif priorty==2:
        index = 7


    instance = DropdownComponentClass()
    instance.clickCheckBox(handle,priorty)
    handle = getHandle(setup,MuralConstants.CREATERULEPOPUP,MuralConstants.ADDRULE)
    instance.doSelectionOnVisibleDropDown(handle,operator,priorty)
    instance.sendkeys_input(number_value, getHandle(setup,MuralConstants.CREATERULEPOPUP,"allNumberInputs"),priorty,"allNumberInputs","number")
    instance.doSelectionOnVisibleDropDown(handle,unitSystem,priorty+1)
    pass

def setTime(setup,startEnd,timeObj):
    pass

def setFilters(setup,index,value):
    pass

def addFilter(setup,buttonName):
    pass


