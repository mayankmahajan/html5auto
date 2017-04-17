from classes.Pages.BasePageClass import *
from classes.Components.MulitpleDropdownComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.TableComponentClass import *

class UserManagementScreenClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.picker = MulitpleDropdownComponentClass()
        self.dropdown = DropdownComponentClass()
        self.table = TableComponentClass()
        # Common Components
        BasePageClass.__init__(self,driver)
