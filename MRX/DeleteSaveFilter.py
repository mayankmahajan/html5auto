import unittest
from Utils.logger import *
from selenium import webdriver
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import os

try:
    newFilterDetails = ConfigManager().getNodeElements("savenewfilter", "filter")

    for k, filterDetail in newFilterDetails.iteritems():
        if 'edit' in filterDetail['filtername'] and filterDetail['button']=='Save':
            setup = SetUp()
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            udScreenInstance = UDScreenClass(setup.d)
            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            UDHelper.editSaveFilter(setup,MRXConstants.LFPOPUP,udScreenInstance,filterDetail)
            setup.d.close()


    for k, filterDetail in newFilterDetails.iteritems():
        if filterDetail['button']=='Save' and filterDetail['isOverwrite']=='True':
            setup = SetUp()
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            udScreenInstance = UDScreenClass(setup.d)
            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            UDHelper.deleteSaveFilter(setup,MRXConstants.LFPOPUP,udScreenInstance,filterDetail)
            setup.d.close()

    newFilterDetails = ConfigManager().getNodeElements("savenewfilter", "filter")
    for k, filterDetail in newFilterDetails.iteritems():
        if filterDetail['button']=='Save' and filterDetail['isOverwrite']=='False':
            filterDetail['filtername']=filterDetail['filtername']+"_new"
            setup = SetUp()
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            udScreenInstance = UDScreenClass(setup.d)
            exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
            udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            UDHelper.deleteSaveFilter(setup, MRXConstants.LFPOPUP, udScreenInstance, filterDetail)
            setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
