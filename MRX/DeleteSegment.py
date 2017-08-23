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
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    column_0_ValueFromTable = segmentScreenInstance.table.getColumnValueFromTable(0, tableHandle)
    Flag=True
    for value in column_0_ValueFromTable:
        if 'auto' in value:
            handle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
            index = segmentScreenInstance.table.getRowIndexFromTable(0, handle, str(value))
            if index!=-1:
                data2 = segmentScreenInstance.table.getTableData1(handle)
                segmentDetailFromTable = []
                for rowvalue in data2['rows'][index]:
                    segmentDetailFromTable.append(rowvalue)

                try:
                    handle['table']['delete'][index].click()
                    confirmPopup=confirm_Popup(setup,str(value),testCaseId='MKR-1700,1701')
                    logger.info('Deleted Segment Details= %s',str(segmentDetailFromTable))
                    resultlogger.info('Deleted Segment Details= %s',str(segmentDetailFromTable))
                except Exception as e:
                    logger.debug("Not able to click on delete for segment = %s ", str(value))
                    resultlogger.debug("Not able to click on delete for segment = %s ", str(value))
                    continue
                if Flag:
                    checkEqualAssert(Constants.USERNAME,segmentDetailFromTable[4],message='only Owned Segments Can be Deleted by a User',testcase_id='MKR-1699')
                    Flag=False

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    for value_1 in column_0_ValueFromTable:
        if 'auto' in value:
            checkEqualAssert(False, tableMap['rows'].has_key(str(value_1)),message='Verify Segment ='+ str(value_1)+" Deleted Successfully",testcase_id='MKR-1701')

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()
