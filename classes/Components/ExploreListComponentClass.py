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
        return True

    def launchModule(self,handlres,text):
        for el in handlres["appHeader"]["alllinks"]:
            if text in el.text:
                el.click()
                return True
        return False


    def switchApp(self,h):
        h['appHeader']['switchertemplate'][0].click()

        # if child==None:
        #     child='cellitem'
        # if parent==None:
        #     parent='switchApp'



    def launchapp(self,h,index,parent="switchApp",child="cellitem"):
        try:
            h[parent][child][index].click()
            return True
        except Exception as e:
            return e