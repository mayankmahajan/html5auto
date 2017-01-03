from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.ContextMenuComponentClass import *


class ReportsModuleClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.dropdown = DropdownComponentClass()
        self.table=TableComponentClass()
        self.cm = ContextMenuComponentClass()
        self.reportpopup = GenerateReportsComponentClass()

        # Common Components
        BasePopClass.__init__(self,driver)

    def launchCreateReport(self,driver):
        try:
            driver.execute_script("document.getElementsByClassName('createReportBtn')[0].click()")
            return True
        except Exception as e:
            return e