from Utils.utility import *
from MuralConstants import *

def setGlobalFilters(globalFilterInstance,setup):
    # globalFilterInstance = GlobalFiltersPopClass(setup.d)

    networkKeys = setup.cM.getAllNodeElements("networkFilters","filter")
    apnratKeys = setup.cM.getAllNodeElements("apnratFilters","filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters","filter")

    networkFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"network"),networkKeys)
    apnratFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"apnrat",True),apnratKeys)
    deviceFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"device",True),deviceKeys)

    expectedFilters = merge_dictionaries(merge_dictionaries(networkFilters,apnratFilters),deviceFilters)

    actualFilters = insertKeys(globalFilterInstance.getToolTipData(setup,getHandle(setup,MuralConstants.GFPOPUP)),networkKeys+apnratKeys+deviceKeys)

    checkEqualDict(expectedFilters,actualFilters,"","","Verify Filters Selections")
    return actualFilters

    # global_network= parseFilters(setup.cM.getNodeElements("globalScreenFilters","network"))
    # global_apnrat= parseFilters(setup.cM.getNodeElements("globalScreenFilters","apnrat"))
    # global_device= parseFilters(setup.cM.getNodeElements("globalScreenFilters","device"))
    # globalfilters= setup.cM.getNodeElements("reportwizardfilters","filter")

    # globalFilterInstance.clickLink(globalfilters['network']['locatorText'],getHandle(setup,MuralConstants.GFPOPUP,MuralConstants.ALLLINKS))

    # networkFilters = setFilters(setup,globalFilterInstance,"network")
    # apnratFilters = setFilters(setup,globalFilterInstance,"apnrat",True)
    # deviceFilters = setFilters(setup,globalFilterInstance,"device",True)

def getGlobalFiltersFromScreen(screenName,globalFilterInstance, setup):
    # globalFilterInstance = GlobalFiltersPopClass(setup.d)

    networkKeys = setup.cM.getAllNodeElements("networkFilters","filter")
    apnratKeys = setup.cM.getAllNodeElements("apnratFilters","filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters","filter")
    actualFilters = insertKeys(globalFilterInstance.getAllSelectedFilters(getHandle(setup,screenName,"filterArea")),networkKeys+apnratKeys+deviceKeys)
    return actualFilters

def insertKeys(dictionary,keys):
    if type(dictionary) == dict:
        for k in keys:
            if k not in dictionary.keys():
                dictionary[k] = []
        return dictionary
    else:
        return dictionary

def createFilterMap(filters,keys):
    return dict(zip(keys,filters))

def getGlobalFiltersToolTipData(screenName,globalFilterInstance,setup):
    networkKeys = setup.cM.getAllNodeElements("networkFilters","filter")
    apnratKeys = setup.cM.getAllNodeElements("apnratFilters","filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters","filter")
    actualFilters = insertKeys(globalFilterInstance.getToolTipData(setup,getHandle(setup,screenName)),networkKeys+apnratKeys+deviceKeys)
    return actualFilters
