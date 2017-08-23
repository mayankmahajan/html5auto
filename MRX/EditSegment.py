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

def verifyEditDetailWithTable(DataFromTable,DataFromUI,edit_info='',testCaseid=''):
    DataFromTable.pop()
    DataFromTable.pop()

    createdon_from_table = DataFromTable.pop()
    createdon_from_UI = DataFromUI.pop()

    checkEqualAssert(createdon_from_UI.split(":")[0], createdon_from_table.split(':')[0], '', '','Verify Creted on from UI..... Expected =' + createdon_from_UI + ' Actual =' + createdon_from_table)
    del DataFromTable[4]
    del DataFromTable[2]

    checkEqualAssert(DataFromTable, DataFromUI, "", "","Verify "+edit_info+" Detail From table",testcase_id=testCaseid)


try:
    setup = SetUp()

    login(setup,Constants.USERNAME,Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN,'allbuttons')

    check_Count=0
    SegmentHelper.checkStatusForAllButtons(segmentScreenHandle,segmentScreenInstance,check_Count,checkButtonStatus=True)

    SegmentHelper.performLogicalOperation(setup,segmentScreenInstance,'Intersect',checkButtonStatus=True)
    SegmentHelper.performLogicalOperation(setup,segmentScreenInstance,'Union',checkButtonStatus=True)
    SegmentHelper.performLogicalOperation(setup,segmentScreenInstance,'Aut',checkButtonStatus=True)



    editSegmentDetails=setup.cM.getNodeElements("editSegmentDetails","segment")
    for k, segmentDetail in editSegmentDetails.iteritems():
        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        data2 = segmentScreenInstance.table.getTableData1(tableHandle,length=20)
        index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['segmentname'])

        if index!=-1:
            segmentDetailFromTable = []
            for value in data2['rows'][index]:
                segmentDetailFromTable.append(value)

            logger.debug("Going to Click Edit/Info Button for segment =%s", segmentDetail['segmentname'])
            resultlogger.debug("Going to Click Edit/Info Button for segment =%s",segmentDetail['segmentname'])

            try:
                tableHandle['table']['info_edit'][index].click()
            except Exception as e:
                logger.debug("Not able to click on edit/info for segment = %s ", segmentDetail['segmentname'])
                resultlogger.debug("Not able to click on edit/info for segment = %s ", segmentDetail['segmentname'])
                checkEqualAssert('Run','Not Run',message='TC related to info/edit not run bcoz edit/info icon not clicked')
                continue

            if segmentDetail['edit_info'] == 'info':
                checkEqualAssert(True,str(segmentDetailFromTable[2]) in ['Rejected','Running'],message="Verify Segment having info instead of edit have Status Running or Rejected ")
                segmentDetailFromUI= SegmentHelper.set_GetDetailFromEdit(setup, segmentScreenInstance,False,segmentDetail)
                verifyEditDetailWithTable(segmentDetailFromTable,segmentDetailFromUI,edit_info='Info',testCaseid='MKR-1698')

            else:
                segmentDetailFromUI = SegmentHelper.set_GetDetailFromEdit(setup, segmentScreenInstance, False, segmentDetail)
                # Verify Value before Edit
                if segmentDetail['button']!='Cancel':
                    verifyEditDetailWithTable(segmentDetailFromTable, segmentDetailFromUI,edit_info='Edit',testCaseid='MKR-1693')

            ###########################Edit Segment####################################################################
            if segmentDetail['edit_info']=='edit':
                tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                data2 = segmentScreenInstance.table.getTableData1(tableHandle,length=20)
                index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['segmentname'])

                segmentDetailFromTable1 = []
                for value in data2['rows'][index]:
                    segmentDetailFromTable1.append(value)

                try:
                    tableHandle['table']['info_edit'][index].click()
                    time.sleep(2)
                except Exception as e:
                    logger.debug("Not able to click on edit for user = %s ", segmentDetail['segmentname'])
                    resultlogger.debug("Not able to click on edit for user = %s ", segmentDetail['segmentname'])
                    checkEqualAssert('Run', 'Not Run',message='TC related to info/edit not run bcoz edit/info icon not clicked')
                    continue

                checkEqualAssert(['Completed',Constants.USERNAME],[str(segmentDetailFromTable1[2]),str(segmentDetailFromTable1[4])],message="Veriy Editable Segment have Completed Status and Owned By Current User",testcase_id='MKR-1692')
                segmentDetailFromUI1 = SegmentHelper.set_GetDetailFromEdit(setup, segmentScreenInstance, True, segmentDetail)

                tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
                if segmentDetail['button']=='Cancel':
                    checkEqualAssert(True, tableMap['rows'].has_key(segmentDetail['segmentname']), "", "","Verify Segment Not Updated if Press Cancel button",testcase_id='MKR-1695')
                    segmentScreenInstance.cm.clickButton('Refresh',getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
                    #tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                    #segmentScreenInstance.table.scrollUpTable(tableHandle, driver=setup)
                else:
                    checkEqualAssert(True, tableMap['rows'].has_key(segmentDetail['newsegmentname']), "", "","Verify Segment Updated Successfully")
                    segmentScreenInstance.cm.clickButton('Refresh', getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
                    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                    #segmentScreenInstance.table.scrollUpTable(tableHandle, driver=setup)
                    index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['newsegmentname'])
                    data2 = segmentScreenInstance.table.getTableData1(tableHandle,length=20)
                    if index==-1:
                        logger.error("Not able to Update Edit Details = %s",segmentDetailFromUI1)
                        raise
                    else:
                        segmentDetailFromTable2 = []
                        for value in data2['rows'][index]:
                            segmentDetailFromTable2.append(value)
                        if len(segmentDetailFromUI1)>0:
                            verifyEditDetailWithTable(segmentDetailFromTable2, segmentDetailFromUI1,edit_info='Edit',testCaseid='MKR-1694')


    setup.d.close()


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s",r,str(e))
    setup.d.close()
