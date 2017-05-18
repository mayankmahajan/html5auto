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

def verifyEditDetailWithTable(DataFromTable,DataFromUI):
    DataFromTable.pop()
    DataFromTable.pop()

    createdon_from_table = DataFromTable.pop()
    createdon_from_UI = DataFromUI.pop()

    checkEqualAssert(createdon_from_UI.split(":")[0], createdon_from_table.split(':')[0], '', '','Verify Creted on from UI..... Expected =' + createdon_from_UI + ' Actual =' + createdon_from_table)
    del DataFromTable[4]
    del DataFromTable[2]

    checkEqualAssert(DataFromTable, DataFromUI, "", "","Verify Edit Segment Detail From table")


setup = SetUp()

login(setup,Constants.USERNAME,Constants.PASSWORD)
segmentScreenInstance = SegmentScreenClass(setup.d)
#tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN,'table')
#segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN)

segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN,'allbuttons')
check_Count=0
SegmentHelper.checkStatusForAllButtons(segmentScreenHandle,segmentScreenInstance,check_Count)

tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
checkBoxForLogicalOp=setup.cM.getNodeElements("selectCheckBoxForPerformLogicalOpertion","segment")

for k, checkboxname in checkBoxForLogicalOp.iteritems():
    index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle,checkboxname['segmentname'] )
    if index!=-1:
        segmentScreenInstance.cm.clickCheckBox(tableHandle,index,parent="table")
        if segmentScreenInstance.cm.isCheckBoxSelected_MRX(tableHandle,index,parent="table"):
            check_Count=check_Count+1
            SegmentHelper.checkStatusForAllButtons(segmentScreenHandle, segmentScreenInstance, check_Count)


if check_Count>1:
    #perform Intersection
    segmentScreenInstance.cm.clickButton("Intersection", segmentScreenHandle)







editSegmentDetails=setup.cM.getNodeElements("editSegmentDetails","segment")
for k, segmentDetail in editSegmentDetails.iteritems():
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    data2 = segmentScreenInstance.table.getTableData1(tableHandle)

    index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['segmentname'])
    segmentDetailFromTable = []
    for value in data2['rows'][index]:
        segmentDetailFromTable.append(value)

    logger.debug("Going to Click Edit/Info Button for segment =%s", segmentDetail['segmentname'])
    resultlogger.debug("Going to Click Edit/Info Button for segment =%s",segmentDetail['segmentname'])

    try:
        tableHandle['table']['info_edit'][index].click()
    except Exception as e:
        logger.debug("Not able to click on edit for segment = %s ", segmentDetail['segmentname'])
        resultlogger.debug("Not able to click on edit for segment = %s ", segmentDetail['segmentname'])
        continue


    segmentDetailFromUI= SegmentHelper.set_GetDetailFromEdit(setup, segmentScreenInstance,False,segmentDetail)
    # Verify Value before Edit
    verifyEditDetailWithTable(segmentDetailFromTable,segmentDetailFromUI)

    #Edit Segment

    if segmentDetail['edit_info']=='edit':
        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['segmentname'])
        try:
            tableHandle['table']['info_edit'][index].click()
        except Exception as e:
            logger.debug("Not able to click on edit for user = %s ", segmentDetail['segmentname'])
            resultlogger.debug("Not able to click on edit for user = %s ", segmentDetail['segmentname'])
            continue

        segmentDetailFromUI = SegmentHelper.set_GetDetailFromEdit(setup, segmentScreenInstance, True, segmentDetail)

        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

        checkEqualAssert(True, tableMap['rows'].has_key(segmentDetail['newsegmentname']), "", "","Verify Segment Updated Successfully ")
        index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['newsegmentname'])
        data2 = segmentScreenInstance.table.getTableData1(tableHandle)
        if index==-1:
            logger.debug("Not able to Update Edit Details = %s",segmentDetailFromUI)
        else:
            segmentDetailFromTable = []
            for value in data2['rows'][index]:
                segmentDetailFromTable.append(value)
            if len(segmentDetailFromUI)>0:
                verifyEditDetailWithTable(segmentDetailFromTable, segmentDetailFromUI)




segmentDetails=setup.cM.getNodeElements("segmentDetails","segment")
flag_Top_segment=True
for k, segmentDetail in segmentDetails.iteritems():
    if segmentDetail['button']!='Cancel':
        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['segmentname'])
        segment_Name = segmentDetail['segmentname']
        if index==-1:
            index = segmentScreenInstance.table.getRowIndexFromTable(0, tableHandle, segmentDetail['newsegmentname'])
            segment_Name = segmentDetail['newsegmentname']
        try:
            tableHandle['table']['delete'][index].click()
            confirm_Popup(setup, segment_Name)
        except Exception as e:
            logger.debug("Not able to click on delete for segment = %s ", segmentDetail['segmentname'])
            resultlogger.debug("Not able to click on delete for segment = %s ", segmentDetail['segmentname'])
            continue




setup.d.close()


# except Exception as e:
#     isError(setup)
#     r = "issue_" + str(random.randint(0, 9999999)) + ".png"
#     setup.d.save_screenshot(r)
#     logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
#     raise e
#     setup.d.close()
