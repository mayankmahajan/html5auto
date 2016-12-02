from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *



class GenerateReportsPopClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.reportspopup=GenerateReportsComponentClass()


        # Common Components
        BasePopClass.__init__(self,driver)

