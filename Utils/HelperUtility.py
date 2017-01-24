import unittest
from Utils.logger import *
from selenium import webdriver
import random
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.SearchComponentClass import *



def ValidateSummarybar(handle,measures,view,screenInstance,obj,pageName):
        #check if selected screen has pie view or btv view
        if view == "pielegend":
            data = screenInstance.pielegend.getData(handle)
            #for pie data is in legendText and index is in data_index
            data_field="legendText"
            data_index="selIndices"
            length = len(data[data_field])
            if length == 1:
                rand = 0
            else:
                rand = random.randrange(0, length)
            #Set selection on pie
            screenInstance.pielegend.setSelection(obj.dH, [rand],handle)
            handle = getHandle(obj,pageName)
            #get the data of selected index
            defselection = screenInstance.pielegend.getSelection(handle)
            data_list = defselection["legendText"][0]

            index = data_list.find('\n')
            name = data_list[0:index]
            value = data_list[index + 1::]

        elif view == "btv":
            data = screenInstance.btv.getData(handle)
            data_field='BTVCOLUMN1'
            data_index = "selIndex"
            length = len(data[data_field])
            rand = random.randrange(1, length)
            screenInstance.btv.setSelection(rand, handle)
            handle = getHandle(obj, pageName)
            defselection = screenInstance.btv.getSelection(handle)
            value = defselection['BTVCOLUMN2']
            name = defselection['BTVCOLUMN1']

        else:
            print "Invalid view"
            exit(1)

        values = measures.split('_')
        try:
            if (values[3] == "average"):
                values[3] = "Average"
        except:
            print "Average is not there"

        try:
            if (values[3] == "peak"):
                values[3] = "Peak"

        except:
            print "Peak is not there"

        if (values[0] == "Wan-Cost($)"):
            values[0] = "Wan Cost($)"
            selections = screenInstance.summarybar.getSelection(handle)
            summarybarvalues = selections[name][values[0]]['Average']

        else:
            selections = screenInstance.summarybar.getSelection(handle)
            summarybarvalues = selections[name][values[0]][values[3]]

        return [value,summarybarvalues,name]







