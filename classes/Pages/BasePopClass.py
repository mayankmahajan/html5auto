from classes.Components.ContextMenuComponentClass import *
from classes.Components.MeasureComponentClass import *
from classes.Components.SummaryBarComponentClass import *
from classes.Components.QuicklinkTimeRangeComponentClass import *
from classes.Components.SearchComponentClass import *
from classes.Components.SwitcherComponentClass import *

class BasePopClass(BaseComponentClass):
    def __init__(self,driver):
        BaseComponentClass.__init__(self)

        self.measure = MeasureComponentClass()
        self.summarybar = SummaryBarComponentClass()
        self.quiklinkTimeRange = QuicklinkTimeRangeComponentClass()
        self.searchComp = SearchComponentClass()
        self.cm = ContextMenuComponentClass()
        self.switcher = SwitcherComponentClass()

    def clickLink(self,value,handle,parent="alllinks",child="a"):
        for el in handle[parent][child]:
            if el.text == value:
                try:
                    logger.info("Going to click link %s",el.text)
                    el.click()
                    return True
                except ElementNotSelectableException or Exception as e:
                    logger.error("Exception found while clicking %s = %s",el.text,e)
                    return e
        logger.error("Link Text not found = %s",el.text)
        return False

    def clickLinkByIndex(self,index,handle,parent="alllinks",child="a"):
        for i in range(len(handle[parent][child])):
            if i == index:
                try:
                    logger.info("Going to click link %s",handle[parent][child][i].text)
                    handle[parent][child][i].click()
                    return handle[parent][child][i].text
                except ElementNotSelectableException or Exception as e:
                    logger.error("Exception found while clicking %s = %s",handle[parent][child][i].text,e)
                    return e
        logger.error("Link Text '%s' not found at index = %s",str(index),handle[parent][child][i].text)
        return False

    def clickLinkByPartialText(self,value,handle,parent="alllinks",child="a"):
        for el in handle[parent][child]:
            if value in el.text:
                try:
                    logger.info("Going to click link %s",el.text)
                    el.click()
                    return el.text
                except ElementNotSelectableException or Exception as e:
                    logger.error("Exception found while clicking %s = %s",el.text,e)
                    return e
        logger.error("Link Text not found = %s",el.text)
        return False



