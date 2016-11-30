from classes.Components.ContextMenuComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.SummaryBarComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.SearchComponentClass import *

class BasePageClass():
    def __init__(self,driver):

        self.measure = MeasureComponentClass()
        self.summarybar = SummaryBarComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.searchComp = SearchComponentClass()
        self.cm = ContextMenuComponentClass()

    def testComponents(self):
        pass

    # def scrollToElement(self,driver,handles):
    # Common Components


