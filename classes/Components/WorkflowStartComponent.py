from classes.Components.BaseComponentClass import *

class WorkflowStartComponentClass(BaseComponentClass):
    def __init__(self):
        BaseComponentClass.__init__(self)

    # def verifyAllText(self,h,parent,child):
    #
    #
    # def verifyAllLinksAvailable(self,h,parent,child):

    @staticmethod
    def launchScreen(name,h,parent="screenbody",child="workflowstart"):
        try:
            for el in h[parent][child][0].find_elements_by_tag_name("dfn"):
                if name in el.text:
                    logger.info("Going to launch = %s",str(el.text))
                    el.click()
                    logger.info("Launched = %s",str(name))
        except Exception as e:
            logger.error("Exception caught while launching = %s",name)
            return e





