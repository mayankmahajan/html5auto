from BasePageClass import BasePageClass
from classes.Components.QuickTrendsComponentClass import *



class QuickTrendsPageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.quicktrends=QuickTrendsComponentClass()


        # Common Components
        BasePageClass.__init__(self,driver)

