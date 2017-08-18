import unittest
from Utils.logger import *
from selenium import webdriver
from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.UDScreenClass import *
from MRXUtils.MRXConstants import *
from classes.Pages.ExplorePageClass import *
from MRXUtils import UDHelper
from MRXUtils import SegmentHelper
import os

def detailFromScreen(setup,screenName,parent='time_measure',child='span'):
    detailFromScreen_Dict={}
    h=getHandle(setup,screenName,parent)
    detailFromScreen_Dict['Source:']='User Distribution'
    detailFromScreen_Dict['Created on:']='-'
    detailFromScreen_Dict['Time range:']=str(h[parent][child][0].text).strip().split('(')[0].strip()
    detailFromScreen_Dict['Metric:'] =str(h[parent][child][1].text).strip()
    return detailFromScreen_Dict


try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")

    UD_Flag=exploreScreenInstance.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
    checkEqualAssert(True,UD_Flag,message="Verify that the User Distribution page gets rendered on clicking on its button",testcase_id='MKR-1755')

    udScreenInstance =UDScreenClass(setup.d)
    selectedView=udScreenInstance.switcher.getMeasureChangeSelectedSwitcher_UD(getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
    checkEqualAssert([0],selectedView,message="Verify that by default chart view is shown on User Distribution page",testcase_id='MKR-1757')

    handlefortimeandmeasure = getHandle(setup, MRXConstants.UDSCREEN, 'time_measure')
    timeRangeFromScreen = str(handlefortimeandmeasure['time_measure']['span'][0].text).strip()
    measureFromScreen = str(handlefortimeandmeasure['time_measure']['span'][1].text).strip()
    checkEqualAssert(True,'Last 7 days' in timeRangeFromScreen,message="Verify that Last 7 Days are default filters on the User Distribution page :: Actual Filter = "+timeRangeFromScreen,testcase_id='MKR-1758')
    checkEqualAssert('Volume', measureFromScreen, message="Verify that Volume are the default filters on the User Distribution page",testcase_id='MKR-1758')

    udScreenInstance.switcher.measureChangeSwitcher_UD(0, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
    chart_view = udScreenInstance.switcher.getMeasureChangeSelectedSwitcher_UD(getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
    UDHelper.getSummaryDetailAndValidatePresenceOfValidationBox(setup, MRXConstants.UDSCREEN,view=chart_view,check=True)

    udScreenInstance.switcher.measureChangeSwitcher_UD(1, getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
    table_view = udScreenInstance.switcher.getMeasureChangeSelectedSwitcher_UD(getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
    UDHelper.getSummaryDetailAndValidatePresenceOfValidationBox(setup, MRXConstants.UDSCREEN, view=table_view,check=True)

    ########################################### CREATE SEGMENT FROM UDP ################################################

    createSegmentDetails = setup.cM.getNodeElements("createSegmentFromUD", "segment")

    checkBlankLoadFilter=True
    beforeCreateSegmentTotalSaveFilter=0

    for k, segmentDetail in createSegmentDetails.iteritems():
        udScreenInstance.switcher.measureChangeSwitcher_UD(1,getHandle(setup, MRXConstants.UDSCREEN, "switcher"))
        udScreenInstance.table.setSpecialSelection(setup.d,[int(segmentDetail['select_row_from']),int(segmentDetail['select_row_to'])], Keys.SHIFT,getHandle(setup, MRXConstants.UDSCREEN, 'table'))
        data =udScreenInstance.table.getSelectedRow(getHandle(setup,MRXConstants.UDSCREEN,'table'))

        expectedSelection=[int(segmentDetail['select_row_from'])*5,int(segmentDetail['select_row_to'])*5]
        actualSelection=[int(data['rows'][0][0].split('-')[1].rstrip(']%')),int(data['rows'][len(data['rows'])-1][0].split('-')[1].rstrip(']%'))]

        checkEqualAssert(expectedSelection,actualSelection,message='Verify that a user is able to select different segments on the table by selecting multiple rows',testcase_id='MKR-1814')

        textFromSummary=UDHelper.verifySummaryWithTable(setup,MRXConstants.UDSCREEN,udScreenInstance,data)
        detailFromScreen_Dict = detailFromScreen(setup, MRXConstants.UDSCREEN)

        if checkBlankLoadFilter:
            h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
            h['filterArea']['toggleicon'][0].click()
            udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
            beforeCreateSegmentTotalSaveFilter=UDHelper.getTotalSaveFilter(setup)
            udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.LFPOPUP, Constants.ALLBUTTONS))

        udScreenInstance.clickButton('Create Segment',getHandle(setup,MRXConstants.UDSCREEN,'summary_validation'),parent='summary_validation')
        addedSegmentDetail, detailFromPopup_Dict, textFromPopUp =UDHelper.createSegmentFromUD(setup,udScreenInstance,segmentDetail)

        checkEqualAssert(textFromSummary,textFromPopUp,message='Verify same text on summary and popup',testcase_id='MKR-1816')
        checkEqualDict(detailFromScreen_Dict,detailFromPopup_Dict,message='Verify Same Detail on Create Segment Popup',testcase_id='MKR-1816')

        exploreScreenInstance.exploreList.launchModule(getHandle(setup,'explore_Screen'), "SEGMENTS")
        time.sleep(8)
        udScreenInstance.cm.clickButton('Refresh', getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))

        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        tableMap = udScreenInstance.table.getTableDataMap(tableHandle, driver=setup)

        if segmentDetail['button'] == 'Cancel':
            checkEqualAssert(False,tableMap['rows'].has_key(segmentDetail['segmentname']),message="Verify that if cancel button is pressed then the segment does not get created",testcase_id='MKR-1871')
            exploreScreenInstance.exploreList.launchModule(getHandle(setup, 'explore_Screen'), "USER DISTRIBUTION")

        if segmentDetail['button']=='Create' and len(addedSegmentDetail)>0:
            checkEqualAssert(True,tableMap['rows'].has_key(segmentDetail['segmentname']),message="Verify Segment added Successfully With Detail= "+str(addedSegmentDetail),testcase_id='MKR-1815')
            tableMap['rows'][segmentDetail['segmentname']].pop()
            tableMap['rows'][segmentDetail['segmentname']].pop()

            createdon_from_table=tableMap['rows'][segmentDetail['segmentname']].pop()
            createdon_from_Popup=addedSegmentDetail.pop()

            status_from_table=tableMap['rows'][segmentDetail['segmentname']][2]
            del tableMap['rows'][segmentDetail['segmentname']][2]
            status_from_Popup=addedSegmentDetail[2]
            del addedSegmentDetail[2]

            if 'Rejected' in status_from_Popup:
                checkEqualAssert(str(status_from_Popup),str(status_from_table),message='Verify Rejected status of new added segment')
            else:
                if str(status_from_table)=='Running':
                    checkEqualAssert('Completed',str(status_from_table),message='Verify status of new added segment (Job may be running Check manually)')
                else:
                    checkEqualAssert('Completed',str(status_from_table),message='Verify status of new added segment')

            checkEqualAssert(str(createdon_from_Popup.split(":")[0]).strip(),str(createdon_from_table.split(':')[0]).strip(),'','','Verify Created on from UI..... Expected ='+createdon_from_Popup+' Actual ='+createdon_from_table)
            checkEqualAssert(tableMap['rows'][segmentDetail['segmentname']], addedSegmentDetail,message="Verify Segment Detail From table, Details ="+str(addedSegmentDetail))

            exploreScreenInstance.exploreList.launchModule(getHandle(setup, 'explore_Screen'), "USER DISTRIBUTION")
            if checkBlankLoadFilter:
                exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
                udScreenInstance.explore.exploreList.clickOnLinkByValue(exploreHandle, Constants.USERNAME)
                exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
                udScreenInstance.explore.exploreList.clickOnLinkByValue(exploreHandle, MRXConstants.Logout)
                time.sleep(5)
                login(setup, Constants.USERNAME, Constants.PASSWORD)
                exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
                udScreenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
                h = getHandle(setup, MRXConstants.UDSCREEN, 'filterArea')
                h['filterArea']['toggleicon'][0].click()
                udScreenInstance.multiDropdown.domultipleSelectionWithNameWithoutActiveDropDown(getHandle(setup, MRXConstants.UDSCREEN, 'filterArea'), 'Load Filter', 0, parent="filterArea",child="multiSelectDropDown")
                afterCreateSegmentTotalSaveFilter = UDHelper.getTotalSaveFilter(setup)
                udScreenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.LFPOPUP, Constants.ALLBUTTONS))
                checkEqualAssert(beforeCreateSegmentTotalSaveFilter,afterCreateSegmentTotalSaveFilter,message=' Validate that when user wants to create segment from the UDR screen , then no blank filters should be added in the load filters list',testcase_id='MKR-3090')
                checkBlankLoadFilter=False

        time.sleep(3)
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
