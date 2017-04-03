from Utils.utility import *
from MuralConstants import *
from classes.Pages.GlobalFiltersPopClass import *

def clickOnfilterIcon(setup,screen):
    logger.info("Clicking on FilterIcon")
    h=getHandle(setup,screen,"filterArea")
    h['filterArea']['filterIcon'][0].click()
    return True

def setGlobalFilters(globalFilterInstance,setup,k='0'):
    # globalFilterInstance = GlobalFiltersPopClass(setup.d)

    networkKeys = setup.cM.getAllNodeElements("networkFilters","filter")
    apnratKeys = setup.cM.getAllNodeElements("apnratFilters","filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters","filter")
    contentKeys = setup.cM.getAllNodeElements("contentFilters","filter")

    networkFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"network",k=k),networkKeys)
    apnratFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"apnrat",True,k=k),apnratKeys)
    deviceFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"device",True,k=k),deviceKeys)
    contentFilters = createFilterMap(globalFilterInstance.setFilters(setup,globalFilterInstance,"content",True,k=k),contentKeys)

    expectedFilters = merge_dictionaries(merge_dictionaries(merge_dictionaries(networkFilters,apnratFilters),deviceFilters),contentFilters)

    #actualFilters = insertKeys(globalFilterInstance.getToolTipData(setup,getHandle(setup,MuralConstants.GFPOPUP)),networkKeys+apnratKeys+deviceKeys)

    #checkEqualDict(expectedFilters,actualFilters,"","","Verify Filters Selections")
    return expectedFilters

def setGlobalFilters_old(globalFilterInstance, setup, k='0'):
    # globalFilterInstance = GlobalFiltersPopClass(setup.d)

    networkKeys = setup.cM.getAllNodeElements("networkFilters", "filter")
    apnratKeys = setup.cM.getAllNodeElements("apnratFilters", "filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters", "filter")

    networkFilters = createFilterMap(globalFilterInstance.setFilters(setup, globalFilterInstance, "network", k=k),
                                         networkKeys)
    apnratFilters = createFilterMap(
            globalFilterInstance.setFilters(setup, globalFilterInstance, "apnrat", True, k=k), apnratKeys)
    deviceFilters = createFilterMap(
            globalFilterInstance.setFilters(setup, globalFilterInstance, "device", True, k=k), deviceKeys)

    expectedFilters = merge_dictionaries(merge_dictionaries(networkFilters, apnratFilters), deviceFilters)

    actualFilters = insertKeys(globalFilterInstance.getToolTipData(setup, getHandle(setup, MuralConstants.GFPOPUP)),
                                   networkKeys + apnratKeys + deviceKeys)

    checkEqualDict(expectedFilters, actualFilters, "", "", "Verify Filters Selections")
    return expectedFilters, actualFilters


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
    contentKeys = setup.cM.getAllNodeElements("contentFilters","filter")
    actualFilters = insertKeys(globalFilterInstance.getAllSelectedFilters(getHandle(setup,screenName,"filterArea")),networkKeys+apnratKeys+deviceKeys+contentKeys)
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
    contentKeys = setup.cM.getAllNodeElements("contentFilters","filter")
    actualFilters = insertKeys(globalFilterInstance.getToolTipData(setup,getHandle(setup,screenName)),networkKeys+apnratKeys+deviceKeys+contentKeys)
    return actualFilters


def sortTable(setup,insatnce,columnName="Name"):

    tableHandle = getHandle(setup, MuralConstants.SubscriberScreen, "table")

    #
    # data1 = reportScreenInstance.table.getTableData1(tableHandle)
    # cdata1 = reportScreenInstance.table.convertDataToDict(data1)

    insatnce.table.sortTable1(tableHandle, columnName)

    tableHandle = getHandle(setup, MuralConstants.SubscriberScreen, "table")

    data2 = insatnce.table.getTableData1(tableHandle)
    columnIndex = insatnce.table.getIndexForValueInArray(data2['header'], columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col, reverse=True), col, "", "", "Checking ColumnName Sort : " + columnName)
    logger.info("Sorted")
    cdata2 = insatnce.table.convertDataToDictWithKeyAsRow(data2)

    return cdata2

