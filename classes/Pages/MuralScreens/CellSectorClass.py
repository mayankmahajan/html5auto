from classes.Pages.BasePageClass import *

from classes.Components.MulitpleDropdownComponentClass import *
# from classes.Components.BTVComponentClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *


class CellSectorClass(BasePageClass):
    def __init__(self, driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.timeBar = TimeRangeComponentClass()
        self.calendar = CalendarComponentClass()
        self.picker = MulitpleDropdownComponentClass()

        self.table = TableComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.dropdown = DropdownComponentClass()

        # Common Components
        BasePageClass.__init__(self, driver)