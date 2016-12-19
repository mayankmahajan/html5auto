from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *



class ReportsModuleClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.dropdown = DropdownComponentClass()


        # Common Components
        BasePopClass.__init__(self,driver)

