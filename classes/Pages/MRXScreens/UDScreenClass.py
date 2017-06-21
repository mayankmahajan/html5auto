from classes.Pages.BasePageClass import *
from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Pages.GlobalFiltersPopClass import *
from classes.Components.TreeComponentClass import *
from classes.Components.TimeRangeComponentClass import *

class UDScreenClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        #self.picker = MulitpleDropdownComponentClass()
        self.dropdown = DropdownComponentClass()
        self.multiDropdown = MulitpleDropdownComponentClass()
        self.table = TableComponentClass()
        self.calendar = CalendarComponentClass()
        self.globalfilter = GlobalFiltersPopClass(driver)
        self.tree = TreeComponentClass(driver)
        self.timeBar = TimeRangeComponentClass()
        self.explore=ExplorePageClass(driver)
        # Common Components
        BasePopClass.__init__(self,driver)
