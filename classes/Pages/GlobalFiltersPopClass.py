# coding=utf-8
from classes.Pages.BasePopClass import BasePopClass
from classes.Components.GenerateReportsComponentClass import *
from classes.Components.DropdownComponentClass import *
from classes.Components.SwitcherComponentClass import *
from classes.Components.RoutersPopUpComponentClass import *
from classes.Components.TableComponentClass import *
from classes.Components.CalendarComponentClass import *
from classes.Components.MulitpleDropdownComponentClass import MulitpleDropdownComponentClass
from MuralUtils.MuralConstants import *
from selenium.webdriver.common.keys import *



class GlobalFiltersPopClass(BasePopClass):
    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.dropdown = DropdownComponentClass()
        self.multiDropdown = MulitpleDropdownComponentClass()
        self.utility = __import__("Utils.utility")

        BasePopClass.__init__(self,driver)

    def getAllSelectedFilters(self,h,parent="filterArea",child="filterText",flag=True):
        filters = {}
        try:
            if not h[parent][child]:
                filters = str(h[parent]['filter'][0].text)
                logger.info("Got Selected Filters as %s",filters)
            else:
                for ele in h[parent][child]:
                    # sleep(2)
                    if flag==True:
                        temp = []
                        # ele.send_keys(Keys.NULL)
                        uifilter = str(ele.text).split(':')
                        for s in uifilter[1].split(","):
                            temp.append(s.strip())
                        filters[uifilter[0].strip()] = temp
                        # sleep(2)

                    else:
                        #for handling : and , for MRX Segment filter

                        #import re
                        #key, value = re.search('([a-zA-Z0-9]+)\s{0,}:\s{0,}([\-a-zA-Z0-9 \:]+)', ele.text).group(1), re.search('([a-zA-Z0-9]+)\s{0,}:\s{0,}([\-a-zA-Z0-9 \:]+)', ele.text).group(2)
                        key_value=(ele.text).split(':', 1)
                        try:
                            filters[str(key_value[0]).strip()] = [str(key_value[1]).strip()]
                        except Exception as e:
                            filters[str(key_value[0]).strip()] = [key_value[1].strip()]
                    # sleep(2)

            return filters
        except Exception as e:
            return e


    def parseFilters(self,global_filter):
        filters = {}
        for id in global_filter.keys():
            filters[id] = self.parseFilter(id,global_filter)
        return filters

    @staticmethod
    def parseFilter(id,global_filter):
        flist = []
        for f in global_filter[str(id)]['filters'].split("::"):
            flist.append(str(f).split(','))
        return flist


    def setFilters(self,setup,globalFilterInstance,tab_name,isCheckBox = False,k = "0"):

        global_filter= self.parseFilters(setup.cM.getNodeElements("globalScreenFilters",tab_name))

        globalfilters= setup.cM.getNodeElements("globalfilters","filter")
        globalFilterInstance.clickLink(
                globalfilters[tab_name]['locatorText'],self.utility.utility.getHandle(setup,MuralConstants.GFPOPUP,MuralConstants.ALLLINKS))

        if isCheckBox and not globalFilterInstance.isCheckBoxEnabled(self.utility.utility.getHandle(setup,MuralConstants.GFPOPUP,MuralConstants.ALLCHECKBOXES),0):
            globalFilterInstance.clickCheckBox(
                self.utility.utility.getHandle(setup,MuralConstants.GFPOPUP,MuralConstants.ALLCHECKBOXES),
                0
            )

        filterSelected = []
        # for k in global_filter.keys():
        for i in range(len(global_filter[k])):
            if len(global_filter[k][i]) == 1 and global_filter[k][i][0] == ' ':
                filterSelected.append([])
                pass
            else:
                try:
                    # globalFilterInstance.multiDropdown.selectRadioButton("APN", getHandle(setup,MuralConstants.GFPOPUP,"radios"), "label")
                    globalFilterInstance.multiDropdown.selectRadioButtonByIndex(i, self.utility.utility.getHandle(setup,MuralConstants.GFPOPUP,"radios"), "label")
                except:
                    pass
                selected  = globalFilterInstance.multiDropdown.domultipleSelectionWithIndex(self.utility.utility.getHandle(setup,MuralConstants.GFPOPUP,"filterPopup"),global_filter[k][i],i)
                if selected != ['']:
                    filterSelected.append(selected)
                else:
                    filterSelected.append([])
                # filterSelected.append(globalFilterInstance.multiDropdown.getSelection(getHandle(setup,MuralConstants.GFPOPUP,"filterPopup"),i))

        return filterSelected

    def getToolTipData(self,setup,h,parent="filterArea",tooltip_parent = "globalfiltertooltip",child="filterText",screenName=MuralConstants.GFPOPUP,flag=True):
        try:
            logger.info("Performing Hover action on Golbal Filter text Area")
            setup.dH.action.move_to_element(h[parent][child][0]).perform()
            tooltipHandle = self.utility.utility.getHandle(setup,screenName,tooltip_parent)
            filters = self.getAllSelectedFilters(tooltipHandle,tooltip_parent,child,flag=flag)
            logger.info("Got Tooltip data = %s",str(filters))
            return filters
        except Exception as e:
            logger.error("Got Exception while getting tooltip data for Global Filters = %s",str(e))
            return e

    def clearGlobalFilters(self,h,parent="filterArea", child="clearIcon"):
        try:
            logger.info("Going to Clear Global Filters")
            h[parent][child][0].click()
            return True
        except Exception as e:
            logger.error("Got Exception while clearing Global Filter = %s",str(e))
            return  e

