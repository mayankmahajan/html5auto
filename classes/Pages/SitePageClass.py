from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.TableComponentClass import *

class SitePageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.btv = BTVComponentClass()
        self.switcher = SwitcherComponentClass()
        self.table = TableComponentClass()
        self.cm = ContextMenuComponentClass()

    def testComponents(self):
        return ""





    # def getSelection(self, handlers):
    #     return self._username.text(handlers)
    #
    # def setUserName(self, handlers, index):
    #     self._username.m_send_keys(elHandle, value)

        # self.

    # def getBTVData(self,btvHandle,col1Handle,col2Handle):
    #     data = self.btv.getData(btvHandle,col1Handle,col2Handle)
    #     # col1 = self.btv.getDataforColumn1(col1Handle)
    #     # col2 = self.btv.getDataForColumn2(col2Handle)
    #     # return dict(zip(col1,col2))
    #     return data


