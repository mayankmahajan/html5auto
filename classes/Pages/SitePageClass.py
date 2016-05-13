from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass

class SitePageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.btv = BTVComponentClass()

    def getBTVData(self,btvHandle,col1Handle,col2Handle):
        data = self.btv.getData(btvHandle,col1Handle,col2Handle)
        # col1 = self.btv.getDataforColumn1(col1Handle)
        # col2 = self.btv.getDataForColumn2(col2Handle)
        # return dict(zip(col1,col2))
        return data


