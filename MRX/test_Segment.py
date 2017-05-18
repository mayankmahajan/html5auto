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



setup = SetUp()

login(setup,Constants.USERNAME,Constants.PASSWORD)
segmentScreenInstance = SegmentScreenClass(setup.d)
segmentScreenHandle = getHandle(setup,MRXConstants.SEGMENTSCREEN,'allbuttons')

#popUpHandle=getHandle(setup,MRXConstants.POPUPSCREEN)
#segmentNameFromUI = segmentScreenInstance.cm.sendkeys_input('Praveen',popUpHandle,0)
#segmentNameFromUI=segmentScreenInstance.cm.getValue_input(popUpHandle,0)
#popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys("/Users/praveen.garg1/Documents/segment_sample.csv")
#segmentScreenInstance.cm.selectRadioButton("Shared",popUpHandle,childDiv="label")
#segmentScreenInstance.cm.getSelectedRadioButtonText(popUpHandle,childDiv="input")
#segmentScreenInstance.cm.clickButton("Import",popUpHandle)


#segmentScreenHandle['table']['delete'][1].click()
#flag=confirm_Popup(setup,'testinvalidfile')


#segmentScreenHandle['table']['edit'][1].click()
#SegmentHelper.getDetailFromEdit(setup,segmentScreenInstance)

#segmentScreenInstance.table.sortTable1(segmentScreenHandle,'Created on')

segmentDetails=setup.cM.getNodeElements("segmentDetails","segment")
flag_Top_segment=True
for k, segmentDetail in segmentDetails.iteritems():
    segmentScreenInstance.cm.clickButton("Import", segmentScreenHandle)
    try:
        segmentDetailFromUIPopup=SegmentHelper.importSegment(setup,segmentScreenInstance,segmentDetail)
        if flag_Top_segment:
            tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN,'table')
            data2 = segmentScreenInstance.table.getTableData1(tableHandle)
            checkEqualAssert(segmentDetail['segmentname'],str(data2['rows'][0][0]),'','','Verify New added segment at Top when table sorted on Created on Column')

    except:
        r = "issue_" + str(random.randint(0, 9999999)) + ".png"
        setup.d.save_screenshot(r)
        logger.debug("Got Exception because of invalid entry for Segment :: Screenshot with name = %s is saved", r)
        resultlogger.debug("Got Exception because of invalid entry for Segment:: Screenshot with name = %s is saved", r)
        getHandle(setup, MRXConstants.POPUPSCREEN,'icons')['icons']['closePopupIcon'][0].click()
        continue

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN,'table')
    tableMap = segmentScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    if segmentDetail['button']=='Import' and len(segmentDetailFromUIPopup)>0:
        checkEqualAssert(True,tableMap['rows'].has_key(segmentDetail['segmentname']),"","","Verify Segment added Successfully ")
        tableMap['rows'][segmentDetail['segmentname']].pop()
        tableMap['rows'][segmentDetail['segmentname']].pop()

        createdon_from_table=tableMap['rows'][segmentDetail['segmentname']].pop()
        createdon_from_UI=segmentDetailFromUIPopup.pop()
        checkEqualAssert(createdon_from_UI.split(":")[0],createdon_from_table.split(':')[0],'','','Verify Creted on from UI..... Expected ='+createdon_from_UI+' Actual ='+createdon_from_table)

        checkEqualAssert(tableMap['rows'][segmentDetail['segmentname']], segmentDetailFromUIPopup, "", "","Verify Segment Detail From table")

# Basic Table Functionality
#SegmentHelper.VerifyBasicTableFuncationality(setup,segmentScreenInstance)

flag=segmentScreenInstance.cm.isCheckBoxSelected_MRX(segmentScreenHandle,1,parent="table")
setup.d.close()


# except Exception as e:
#     isError(setup)
#     r = "issue_" + str(random.randint(0, 9999999)) + ".png"
#     setup.d.save_screenshot(r)
#     logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
#     raise e
#     setup.d.close()
