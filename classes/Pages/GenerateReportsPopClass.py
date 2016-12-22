from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *



class GenerateReportsPopClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.reportspopup = GenerateReportsComponentClass()
        self.dropdown = DropdownComponentClass()
        self.switcher = SwitcherComponentClass()


        # Common Components
        BasePopClass.__init__(self,driver)

