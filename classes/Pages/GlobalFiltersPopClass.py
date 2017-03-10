from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.RoutersPopUpComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.MulitpleDropdownComponentClass import MulitpleDropdownComponentClass



class GlobalFiltersPopClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.dropdown = DropdownComponentClass()
        self.multiDropdown = MulitpleDropdownComponentClass()

        BasePopClass.__init__(self,driver)

    def getAllSelectedFilters(self,h,parent="filterPopup",child="allfilters"):
        return [e.text for e in h[parent][child] if e.is_displayed()]


    def getFiltersAtReviewPage(self,h,parent="generateReportDialog",child="filters"):
        tempArray = h[parent][child][0].text.split("\n")[1:-1]
        return self.getFormattedFilters(tempArray)





