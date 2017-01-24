from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.SearchComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.SummaryBarComponentClass import *
class NeNePageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.btv = BTVComponentClass()
        self.measure = MeasureComponentClass()
        self.switcher = SwitcherComponentClass()
        self.cm = ContextMenuComponentClass()
        self.searchComp = SearchComponentClass()
        self.summarybar = SummaryBarComponentClass()
    def testComponents(self):
        return ""