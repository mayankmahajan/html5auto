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

        # Common Components
        BasePopClass.__init__(self,driver)

