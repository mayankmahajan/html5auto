from classes.Components.BaseComponentClass import *


class ExploreListComponentClass(BaseComponentClass):

    def getHandlertoPage(self,elHandler,page):
        for elHandler in exploreListHandler:
            if elHandler.text.upper() in page:
                explorePage.launchPage(elHandler)
                break

    def clickPage(self,elHandler,page):
        pass


