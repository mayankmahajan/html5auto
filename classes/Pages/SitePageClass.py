from BasePageClass import BasePageClass
from classes.Components.BTVComponentClass import BTVComponentClass
from classes.Components.ContextMenuComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.MeasureComponentClass import *
#from classes.Components.PieLegendComponentClass import *
#from classes.Components.PieComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.SearchComponentClass import *
class SitePageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.btv = BTVComponentClass()
        self.switcher = SwitcherComponentClass()
        self.table = TableComponentClass()
        self.cm = ContextMenuComponentClass()
        self.measure = MeasureComponentClass()
        #self.pielegend = PieLegendComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.searchComp = SearchComponentClass()

        # Common Components
        BasePageClass.__init__(self,driver)


    def testComponents(self):
        return ""
