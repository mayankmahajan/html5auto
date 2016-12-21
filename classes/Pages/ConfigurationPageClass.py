from BasePageClass import BasePageClass
from classes.Components.BaseComponentClass import *
from classes.Components.ExploreListComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.IBLeftColumnComponentClass import *

class ConfigurationPageClass(BasePageClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.table = TableComponentClass()
        self.dummyelement = DropdownComponentClass()
        self.leftColumn = IBLeftColumnComponentClass()

        BasePageClass.__init__(self,driver)



    
