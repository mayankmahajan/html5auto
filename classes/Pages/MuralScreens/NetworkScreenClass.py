from classes.Pages.BasePageClass import *

from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.BTVComponentClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *


class NetworkScreenClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.btv = BTVComponentClass()
        self.picker = MulitpleDropdownComponentClass()
        self.timeBar = TimeRangeComponentClass()
        self.calendar =  CalendarComponentClass()
        self.dropdown = DropdownComponentClass()
        self.switcher = SwitcherComponentClass()

        # Common Components
        BasePageClass.__init__(self,driver)
