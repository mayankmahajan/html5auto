from classes.Components.BaseComponentClass import *


class ExploreListComponentClass(BaseComponentClass):


    def getHandlerToPage(self,listHandler,page):
        for elHandler in listHandler:
            if elHandler.text.upper() in page:
                return elHandler
        return False

    def launchScreen(self,handlres,parent,child):
        # h = self.compHandlers(parent,handlres)
        handlres[parent][child][0].click()

    def launchModule(self,handlres,text):
        for el in handlres["appHeader"]["alllinks"]:
            if text in el.text:
                el.click()
                break

    def switchApp(self,h,index,parent=None,child=None):
        if child==None:
            child='cellitem'
        if parent==None:
            parent='switchApp'

        h[parent][child][index].click()

