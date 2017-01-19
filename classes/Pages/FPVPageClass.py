from BasePageClass import BasePageClass
from classes.Components.SearchComponentClass import *
from classes.Components.FPVComponentClass import *

class FPVPageClass(BasePageClass):
    def __init__(self, driver):
        '''
        Constructor
        '''
        self.driver = driver

        self.fpv = FPVComponentClass()
        BasePageClass.__init__(self,driver)



