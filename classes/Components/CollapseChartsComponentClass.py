from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *

class CollapseChartsComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def getSelectedData(self,h,parent,child=None):
        arr = []
        for i in range(len(h[parent]['displayname'])):
            temp = []
            temp.append(h[parent]['displayname'][i].text)
            temp.append(h[parent]['dynamictext'][i].text)
            arr.append(temp)

        return arr

