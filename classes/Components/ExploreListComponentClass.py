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

    # def launchModule(self,handlres,text):
    #     for el in handlres["appHeader"]["alllinks"]:
    #         if text in el.text:
    #             el.click()
    #             break

    def launchModule(self,handlres,text):
        try:
            for el in handlres["appHeader"]["alllinks"]:
                if text in el.text:
                    el.click()
                    return True
        except Exception as e:
            logger.error("Exception found while clicking Module with Title = %s", str(text))
            return e

        logger.debug("Module with title = %s not found", str(text))
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
            time.sleep(10)
            # adding only to make whole suite faster. We can give lesser timeout time for all components
            # this a page load and it takes longer time
            return True
        except Exception as e:
            return e

    def launchappByName(self,h,value,parent="switchApp",child="apps"):
        try:
            for i in range(len(h[parent][child])):
                if str(value)==str(h[parent][child][i].text).strip():
                    h[parent][child][i].click()
                    time.sleep(10)
                    # adding only to make whole suite faster. We can give lesser timeout time for all components
                    # this a page load and it takes longer time
                    return True
            return False
        except Exception as e:
            return e

    def getAllApps(self,h,parent="switchApp",child="apps"):
        list=[]
        for i in range(len(h[parent][child])):
            list.append(str(h[parent][child][i].text).strip())
        return list
