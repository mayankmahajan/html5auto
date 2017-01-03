from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.RoutersPopUpComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.MulitpleDropdownComponentClass import MulitpleDropdownComponentClass



class GenerateReportsPopClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.reportspopup = GenerateReportsComponentClass()
        self.dropdown = DropdownComponentClass()
        self.switcher = SwitcherComponentClass()
        self.routerpopup = RoutersPopUpComponentClass()
        self.routertable = TableComponentClass()
        self.calendar = CalendarComponentClass()
        self.multiDropdown = MulitpleDropdownComponentClass()




        # Common Components
        BasePopClass.__init__(self,driver)

