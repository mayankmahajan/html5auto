from classes.Pages.BasePageClass import *
from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *

class SegmentScreenClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.picker = MulitpleDropdownComponentClass()
        self.dropdown = DropdownComponentClass()
        self.table = TableComponentClass()
        self.calendar = CalendarComponentClass()
        self.globalfilter = GlobalFiltersPopClass(driver)
        # Common Components
        BasePageClass.__init__(self,driver)
