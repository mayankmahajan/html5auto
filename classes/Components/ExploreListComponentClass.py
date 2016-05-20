from classes.Components.BaseComponentClass import *


class ExploreListComponentClass(BaseComponentClass):


    def getHandlerToPage(self,listHandler,page):
        for elHandler in listHandler:
            if elHandler.text.upper() in page:
                return elHandler
        return False


