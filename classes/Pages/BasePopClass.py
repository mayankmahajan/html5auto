from classes.Components.ContextMenuComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.SummaryBarComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.SearchComponentClass import *
from classes.Components.SwitcherComponentClass import *

class BasePopClass():
    def __init__(self,driver):
        pass


        self.measure = MeasureComponentClass()
        self.summarybar = SummaryBarComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.searchComp = SearchComponentClass()
        self.cm = ContextMenuComponentClass()
        self.switcher = SwitcherComponentClass()

    def clickLink(self,value,handle,parent="alllinks",child="a"):
        for el in handle[parent][child]:
            if el.text == value:
                try:
                    el.click()
                    return True
                except ElementNotSelectableException or Exception as e:
                    return e

