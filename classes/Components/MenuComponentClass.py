from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager
from Utils.logger import *

class MenuComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def setSwitcher(self,index,h,parent,child):
        try:
            h[parent][child][0].find_elements_by_tag_name('label')[2].click()
            return True
        except Exception:
            raise Exception
            return Exception
