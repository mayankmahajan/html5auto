import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from MRXUtils.MRXConstants import *
from MRXUtils import SegmentHelper


try:

    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN)
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    data2 = segmentScreenInstance.table.getTableData1(tableHandle)

    click_status=SegmentHelper.clickOnfilterIcon(setup,MRXConstants.SEGMENTSCREEN,'nofilterIcon')
    checkEqualAssert(True,click_status,'','','Verify that "Filter" button just above the Segment table is clickable',testcase_id='MKR-1675')
########################################################################################################################
    filterScreenHandle=getHandle(setup,"filter_Screen")
    checkEqualAssert("Filters",str(filterScreenHandle['allspans']['span'][0].text),'','',"Verify Filter Header Text on Filter Popup")
    allSpanList = []
    for ele in filterScreenHandle['allspans']['span']:
        allSpanList.append(ele.text)
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    checkEqualAssert(True, set(Keys) < set(allSpanList),message='Verify available Filter Expected= ' + str(Keys) + ' Actual Available Set= ' + str(allSpanList),testcase_id='MKR-1676')
########################################################################################################################
    availableButtonList=[]
    for button in filterScreenHandle['allbuttons']['button']:
        availableButtonList.append(str(button.text))
    availableButtonList.append(str(len(filterScreenHandle['icons']['closePopupIcon'])))
    actualButtonList=['Apply Filters','Cancel','Clear All','1']
    checkEqualAssert(actualButtonList,availableButtonList,'','','Verify available button on filter screen',testcase_id='MKR-1677')
########################################################################################################################

    expected = SegmentHelper.setSegmentFilter(setup,segmentScreenInstance,k=0)
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    isError(setup)
    popUpTooltipData = SegmentHelper.getGlobalFiltersToolTipData(MRXConstants.SEGMENTSCREEN, segmentScreenInstance, setup,flag=False)
    checkEqualDict(popUpTooltipData, expected, "", "", "Verify Filters Selections from Tooltip on Segment Screen",testcase_id='MKR-1676,1681')
########################################################################################################################

    filterFromScreen=SegmentHelper.getGlobalFiltersFromScreen(MRXConstants.SEGMENTSCREEN, segmentScreenInstance, setup,flag=False)
    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN,'filterIcon')
    expectedFromFilterPopUp = SegmentHelper.getSegmentFilter(setup, segmentScreenInstance)
    checkEqualDict(filterFromScreen, expectedFromFilterPopUp, "", "", "Verify Filters Selections from Segment Screen")
    segmentScreenInstance.cm.clickButton("Clear All", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    expectedFromFilterPopUpAfterClear = SegmentHelper.getSegmentFilter(setup, segmentScreenInstance)

    BlankDict=SegmentHelper.insertKeys({},Keys)
    checkEqualDict(BlankDict,expectedFromFilterPopUpAfterClear,message='Verify Clear all Functionality for Filter on Popup Screen',testcase_id='MKR-1678')
    segmentScreenInstance.cm.clickButton("Apply Filters", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    data3 = segmentScreenInstance.table.getTableData1(tableHandle)
    checkEqualAssert(data2['rows'], data3['rows'],message='Checked Clear all Functionality for Filter on Segment Screen by verify number of segment visible', testcase_id='MKR-1678')
########################################################################################################################

    SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    expected = SegmentHelper.setSegmentFilter(setup, segmentScreenInstance, k=1)
    try:
        click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN,'closePopupIcon',parent='icons')
    except:
        try:
            click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.FILTERSCREEN, 'closePopupIcon',parent='icons')
        except:
            pass

    if click_status:
        checkEqualAssert(0,len(getHandle(setup,MRXConstants.FILTERSCREEN,'icons')['icons']['closePopupIcon']),message='On pressing the "X", the filter window dissappears',testcase_id='MKR-1679')
        filterFromScreenAfterClear=SegmentHelper.getGlobalFiltersFromScreen(MRXConstants.SEGMENTSCREEN, segmentScreenInstance, setup,flag=False)
        checkEqualAssert('Filters', str(filterFromScreenAfterClear), '', '', 'After press cross (X) no filter should be on Segment Screen',testcase_id='MKR-1679')

    click_status = SegmentHelper.clickOnfilterIcon(setup, MRXConstants.SEGMENTSCREEN, 'nofilterIcon')
    segmentScreenInstance.cm.clickButton("Cancel", getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons'))
    checkEqualAssert(0, len(getHandle(setup, MRXConstants.FILTERSCREEN, 'allbuttons')['allbuttons']['button']), message='On pressing the "Cancel" button the filter window dissappears',testcase_id='MKR-1679')

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()
