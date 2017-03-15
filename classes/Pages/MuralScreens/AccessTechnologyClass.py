from classes.Pages.BasePageClass import *

from classes.Components.MulitpleDropdownComponentClass import *
#from classes.Components.BTVComponentClass import *
from classes.Components.TimeRangeComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.PieComponentClass import *
from classes.Components.PieLegendComponentClass import *
from classes.Components.SummaryBarComponentClass import *


class AccessTechnolohyScreenClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        #self.btv = BTVComponentClass()
        self.picker = MulitpleDropdownComponentClass()
        self.timeBar = TimeRangeComponentClass()
        self.calendar = CalendarComponentClass()
        self.dropdown = DropdownComponentClass()
        self.switcher = SwitcherComponentClass()
        self.piecomponent= PieComponentClass()
        self.pielegend= PieLegendComponentClass()
        self.summarybar= SummaryBarComponentClass()


        # Common Components
        BasePageClass.__init__(self,driver)