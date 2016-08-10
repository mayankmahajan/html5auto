from BaseComponentClass import BaseComponentClass
from Utils.ConfigManager import ConfigManager

class SwitcherComponentClass(BaseComponentClass):

    def __init__(self):
        BaseComponentClass.__init__(self)
        self.configmanager = ConfigManager()


    def doSingleSelection(self):
        BaseComponentClass.click()

    def setSelection(self,index,h):
        data = {}
        toSelect = 'Chart' if index==0 else 'Table'
        handlers = self.compHandlers('switcherView',h)
        for key,value in handlers.iteritems():
            if toSelect.upper() in key.upper():
                if self.configmanager.componentSelectors[key]["action"] == "click":
                    for i in range(len(handlers[key]),0,-1):
                        if handlers[key][i-1].is_displayed():
                            handlers[key][i-1].click()
                            return handlers[key][i-1].text

    def getSelection(self,h):
        data = {}
        handlers = self.compHandlers('switcherView',h)
        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "click":
                # for i in range(0,len(handlers)):
                if handlers[key][len(handlers[key]) - 1].is_displayed() and 'SELECTED' in handlers[key][len(handlers[key]) - 1].get_attribute('class').upper():
                    return handlers[key][len(handlers[key]) - 1].text

