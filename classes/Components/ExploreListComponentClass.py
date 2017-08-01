from classes.Components.BaseComponentClass import *


class ExploreListComponentClass(BaseComponentClass):


    def getHandlerToPage(self,listHandler,page):
        for elHandler in listHandler:
            if elHandler.text.upper() in page:
                return elHandler
        return False

    def clickOnHelpIcon(self,handlres,parent,child):
        try:
            for handle in handlres[parent][child]:
                if len(handle.find_elements_by_tag_name('img'))>0:
                    if 'help' in handle.find_elements_by_tag_name('img')[0].get_attribute('src'):
                        handle.click()
                        return True
        except Exception as e:
            logger.error("Exception found while clicking on HelpIcon")
            return e

        logger.debug("HelpIcon Not Found")
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


    def clickOnLinkByValue(self,exploreHandle,value, parent='appHeader', child='alllinks'):
        try:
            for i in range(len(exploreHandle[parent][child])):
                if str(exploreHandle[parent][child][i].text) == str(value):
                    exploreHandle[parent][child][i].click()
                    return True
            return False
        except Exception as e:
            logger.error("Not able to click on %s", value)
            logger.error("Got Exception <method> %s", str(e))
            resultlogger.error("Not able to click on %s", value)
            return False