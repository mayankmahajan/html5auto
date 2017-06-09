# coding=utf-8
from Utils.utility import *
from MRXUtils.MRXConstants import *
from classes.Pages.MRXScreens.SegmentScreenClass import *



def findPropertyColor(screenInstance,h,property,parent="allinputs",child="input",index=0):
    propertycolor=str(h[parent][child][index].value_of_css_property(property))
    return screenInstance.cm.rgb_to_hex(propertycolor)


def isColorValid(screenInstance, h, property, parent="allinputs", child='input', index=0):
    bordercolor=findPropertyColor(screenInstance,h, property,parent=parent,child=child,index=index)
    if str(bordercolor)==Constants.REDCOLOR:
        logger.debug(" %s is Not valid ",h[parent][child][index].get_attribute('value'))
        return False
    else:
        return True

def dumpResultForButton(condition,request,screenInstance,setup,screen=MRXConstants.POPUPSCREEN,button_label="Import"):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, screen,"allbuttons"))
    if screen==MRXConstants.FILTERSCREEN:
        checkEqualAssert(condition,button_status,"","","Checking State of "+button_label+" for Fields entered : "+str(request),testcase_id='MKR-1680')

    checkEqualAssert(condition, button_status, "", "","Checking State of " + button_label + " for Fields entered : " + str(request))
    return button_status

def VerifyBasicTableFuncationality(setup,screenInstance,parent='table'):

    # header = setup.cM.getNodeElements("segment_Table_Header","column")
    # header_list = []
    # for k, columnname in header.iteritems():
    #     header_list.append(columnname['locatorText'])

    header_list = ['SegmentName','#Users','Status','Source','Owner','Access','Created on','Edit/Info','Delete']

    columns = setup.cM.getNodeElements("segmentsorttablecolumn", "column")
    column_names = []
    for k, column in columns.iteritems():
        column_names.append(column['locatorText'])

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, parent)
    tableMap = screenInstance.table.getTableDataMap(tableHandle,driver=setup,colIndex=-1)
    checkEqualAssert(header_list,tableMap['header'],'','','Verify Table Header on Segment Screen',testcase_id='MKR-1658')

    if tableMap['rows'] == Constants.NODATA:
        logger.info("*********Table Data Not Present************")
        return

    for columnname in column_names:
        sortedData = sortTable(setup, screenInstance, columnName=columnname)
        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnname)

        for k, v in sortedData.iteritems():
            if tableMap['rows'].has_key(k):
                checkEqualAssert(tableMap['rows'][k], sortedData[k],"", "","verify sorted Table rows present in table with key : " + k)
            else:
                logger.info("********table not contain row with key********* : " + k)



def sortTable(setup,insatnce,columnName="Name"):
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, "table")
    insatnce.table.sortTable1(tableHandle, columnName)
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, "table")

    data2 = insatnce.table.getTableData1(tableHandle)
    columnIndex = insatnce.table.getIndexForValueInArray(data2['header'], columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col, reverse=True), col, "", "", "Verify Sorting For ColumnName ="+columnName,testcase_id='MKR-1691')
    logger.info("Sorted")
    cdata2 = insatnce.table.convertDataToDictWithKeyAsRow(data2)
    return cdata2


def set_GetDetailFromEdit(setup,screenInstance,isSetEdit,segment_Input):
    popUpDetails=[]

    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    if segment_Input['edit_info']=='edit':
        checkEqualAssert(MRXConstants.EDITHEADERINEDITPOPUP,str(popUpHandle['allspans']['span'][0].text),'','','Verify Edit Header in Popup')
    elif segment_Input['edit_info']=='info':
        checkEqualAssert(MRXConstants.INFOHEADERINPOPUP, str(popUpHandle['allspans']['span'][0].text), '', '','Verify Info Header in Popup')
        checkEqualAssert('Segment creation failed as there were 0 subscribers',str(popUpHandle['allspans']['span'][9].text),message='Verify message on Info in case of Status=Rejected')
    import re

    if isSetEdit and segment_Input['edit_info']=='edit':
        popUpDetails.append(screenInstance.cm.sendkeys_input(segment_Input['newsegmentname'], popUpHandle, 0))
        popUpDetails.append(re.findall('[0-9]*',str(popUpHandle['allspans']['span'][5].text))[0])
        popUpDetails.append(str(popUpHandle['allspans']['span'][2].text))

        if screenInstance.cm.selectRadioButton(segment_Input['access'],popUpHandle,childDiv="label"):
            popUpDetails.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))
        else:
            popUpDetails.append('Not able to Click Radio Button')

    elif segment_Input['edit_info']=='info':
        popUpDetails.append(str(popUpHandle['allspans']['span'][6].text))
        popUpDetails.append('0')
        popUpDetails.append(str(popUpHandle['allspans']['span'][2].text))
        popUpDetails.append(str(popUpHandle['allspans']['span'][8].text))
    else:
        popUpDetails.append(str(screenInstance.cm.getValue_input(popUpHandle, 0)))
        popUpDetails.append(re.findall('[0-9]*', str(popUpHandle['allspans']['span'][5].text))[0])
        popUpDetails.append(str(popUpHandle['allspans']['span'][2].text))
        popUpDetails.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))

    popUpDetails.append(str(popUpHandle['allspans']['span'][4].text))

    if segment_Input['edit_info']=='edit' and str(segment_Input['button']) == "Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(str(segment_Input['button']), popUpHandle)
        return []


    if segment_Input['edit_info']=='info' or segment_Input['edit_info']=='edit'and  not isSetEdit:
        logger.info('Going to Click on Cross (X) Button')
        popUpHandle['icons']['closePopupIcon'][0].click()
        try:
            popUpHandle['icons']['closePopupIcon'][0].click()
        except:
            pass
        return popUpDetails

    if str(segment_Input['button']) == 'Update':
        logger.info('Going to Click on %s Button ', segment_Input['button'])
        click_status = screenInstance.cm.clickButton(str(segment_Input['button']), popUpHandle)
        checkEqualAssert(True, click_status, "", "","Verify whether " + segment_Input['button'] + " button clicked or not")
        logger.info("********Folowing Updated Data added into table =%s ************", popUpDetails)
        return popUpDetails

##############################################################################################################################

def importSegment(setup,screenInstance,segment_Input,source='Import'):

    flag_segmentname = False
    flag_filepath = False
    segmentDetailFromUI=[]
    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)

    logger.info('Going to Enter Segment Name = %s',segment_Input['segmentname'])
    resultlogger.info('Going to Enter Segment Name = %s',segment_Input['segmentname'])
    #segmentDetailFromUI['Segment Name'] = str(screenInstance.cm.sendkeys_input(segment_Input['segmentname'],popUpHandle,0))
    segmentDetailFromUI.append(str(screenInstance.cm.sendkeys_input(segment_Input['segmentname'],popUpHandle,0)))

    # if not isColorValid(screenInstance, popUpHandle,property=Constants.BORDERCOLOR, index=0):
    #     raise
    flag_segmentname=True
    dumpResultForButton(flag_segmentname and flag_filepath, "Segment Name", screenInstance,setup)

    segmentDetailFromUI.append(segment_Input['uniquecount'])

    segmentDetailFromUI.append(segment_Input['status'])
    segmentDetailFromUI.append(source)
    segmentDetailFromUI.append(Constants.USERNAME)

    #segmentDetailFromUI['Source']='Import'
    #segmentDetailFromUI['# User'] = segment_Input['uniquecount']
    #segmentDetailFromUI['Owner'] = Constants.USERNAME

    logger.info('Going to Enter Access = %s', segment_Input['access'])
    resultlogger.info('Going to Enter Access = %s', segment_Input['access'])

    if screenInstance.cm.selectRadioButton(segment_Input['access'],popUpHandle,childDiv="label"):
        #segmentDetailFromUI['Access'] =str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input"))
        segmentDetailFromUI.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))
    else:
        #segmentDetailFromUI['Access'] = 'Not able to Click Radio Button'
        segmentDetailFromUI.append('Not able to Click Radio Button')

    logger.info('Going to Select .csv File from path= %s', segment_Input['file'])
    resultlogger.info('Going to Select .csv File form path = %s', segment_Input['file'])
    fileDir =find_realPath(segment_Input['file'])
    popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(str(fileDir))

    checkEqualAssert(False,'No File' in str(popUpHandle['footerText']['text'][0].text),message="Verify File Selected from Path  => " + str(fileDir))
    flag_filepath=not 'No File' in str(popUpHandle['footerText']['text'][0].text)
    button_status=dumpResultForButton(flag_segmentname and flag_filepath, "Select .CSV File", screenInstance,setup)

    import datetime
    utc = datetime.datetime.utcnow()
    dateString=utc.strftime(MRXConstants.TIMEPATTERN)

    segmentDetailFromUI.append(str(dateString))


    if not button_status:
        logger.info("*************Import Button not enable**********")
        raise

    if button_status and str(segment_Input['button']) == "Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(str(segment_Input['button']), popUpHandle)
        return []


    if str(segment_Input['button'])=='Import':
        logger.info('Going to Click on %s Button ', segment_Input['button'])
        click_status = screenInstance.cm.clickButton(str(segment_Input['button']),popUpHandle)
        checkEqualAssert(True, click_status, "", "", "Verify whether " + segment_Input['button'] + " button clicked or not")
        # isError(setup)
        logger.info("********Folowing Data added into table =%s ************",segmentDetailFromUI)
        return segmentDetailFromUI

##############################################################################################################################

def logicalOperationSegment(setup,screenInstance,input_Detail,segmentname,access,count,operation):

    flag_segmentname = False
    segmentDetailFromUI=[]

    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    checkEqualAssert(operation+" Segment", str(popUpHandle['allspans']['span'][0].text), '', '','Verify Import Segment Header in Import Popup')

    logger.info('Going to Enter Segment Name = %s when perform =%s',segmentname,operation)
    resultlogger.info('Going to Enter Segment Name = %s when perform =%s',segmentname,operation)
    segmentDetailFromUI.append(str(screenInstance.cm.sendkeys_input(segmentname,popUpHandle,0)))

    flag_segmentname=True
    button_status=dumpResultForButton(flag_segmentname, "Segment Name", screenInstance,setup,button_label="Create")

    segmentDetailFromUI.append(count)

    if int(count)==0:
        segmentDetailFromUI.append('Rejected')
    else:
        segmentDetailFromUI.append('Completed')


    segmentDetailFromUI.append(operation)
    segmentDetailFromUI.append(Constants.USERNAME)

    default_access=str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input"))
    if 'tersect' in operation:
        checkEqualAssert('Private',default_access,message='default the newly created intersect segment has private access',testcase_id='MKR-1718')
    if 'nion' in operation:
        checkEqualAssert('Private',default_access,message='default the newly created union segment has private access',testcase_id='MKR-1726')
    if 'Aut' in operation or 'aut' in operation:
        checkEqualAssert('Private',default_access,message='default the newly created aut segment has private access',testcase_id='MKR-1734')


    logger.info('Going to Enter Access = %s', access)
    resultlogger.info('Going to Enter Access = %s', access)
    if screenInstance.cm.selectRadioButton(access,popUpHandle,childDiv="label"):
        segmentDetailFromUI.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))
    else:
        segmentDetailFromUI.append('Not able to Click Radio Button')


    import datetime
    utc = datetime.datetime.utcnow()
    dateString=utc.strftime(MRXConstants.TIMEPATTERN)
    segmentDetailFromUI.append(str(dateString))


    if not button_status:
        logger.info("*************Import Button not enable**********")
        raise

    if button_status and str(input_Detail['button']) == "Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(str(input_Detail['button']), popUpHandle)
        return []


    if str(input_Detail['button'])=='Create':
        logger.info('Going to Click on %s Button ', input_Detail['button'])
        click_status = screenInstance.cm.clickButton(str(input_Detail['button']),popUpHandle)
        checkEqualAssert(True, click_status, "", "", "Verify whether " + str(input_Detail['button']) + " button clicked or not")
        isError(setup)
        logger.info("********Folowing Data added into table =%s ************",segmentDetailFromUI)
        return segmentDetailFromUI
##################################################################################################################################

def verifyEntryEditSuccessfully(setup,screenInstance,inputDetail,segmentDetailFromUIPopup,addedValue,testCaseId='',testCaseId_1=''):

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    tableMap = screenInstance.table.getTableDataMap(tableHandle, driver=setup)
    if inputDetail['button']=='Cancel' and 'tersect' in addedValue:
        checkEqualAssert(False, tableMap['rows'].has_key(str(addedValue)), "", "", "Verify that on clicking on the Cancel button while creating an Intersection segment the operation gets cancelled and no new segment gets created",testcase_id='MKR-1717')
    if inputDetail['button'] == 'Cancel' and 'nion' in addedValue:
        checkEqualAssert(False, tableMap['rows'].has_key(str(addedValue)), "", "","Verify that on clicking on the Cancel button while creating an Union segment the operation gets cancelled and no new segment gets created",testcase_id='MKR-1725')
    if inputDetail['button'] == 'Cancel' and 'autoAut' in addedValue:
        checkEqualAssert(False, tableMap['rows'].has_key(str(addedValue)), "", "","Verify that on clicking on the Cancel button while creating an Aut segment the operation gets cancelled and no new segment gets created",testcase_id='MKR-1733')

    if inputDetail['button']=='Create' and len(segmentDetailFromUIPopup)>0:
        checkEqualAssert(True,tableMap['rows'].has_key(str(addedValue)),"","","Verify Segment added Successfully",testcase_id=testCaseId_1)
        if 'tersect' in addedValue:
            checkEqualAssert('Intersection',tableMap['rows'][addedValue][3],message='default the newly created Intersect segment has Source as Intersection',testcase_id='MKR-1718')
        if 'nion' in addedValue:
            checkEqualAssert('Union',tableMap['rows'][addedValue][3],message='default the newly created Union segment has Source as Union',testcase_id='MKR-1726')
        if 'autoAut' in addedValue:
            checkEqualAssert('Aut',tableMap['rows'][addedValue][3],message='default the newly created Aut segment has Source as Aut',testcase_id='MKR-1734')

        tableMap['rows'][addedValue].pop()
        tableMap['rows'][addedValue].pop()

        createdon_from_table=tableMap['rows'][addedValue].pop()
        createdon_from_UI=segmentDetailFromUIPopup.pop()
        checkEqualAssert(createdon_from_UI.split(":")[0],createdon_from_table.split(':')[0],'','','Verify Created on from UI..... Expected ='+createdon_from_UI+' Actual ='+createdon_from_table)
        checkEqualAssert(tableMap['rows'][addedValue], segmentDetailFromUIPopup, "", "","Verify Segment Detail From table= "+str(segmentDetailFromUIPopup),testcase_id=testCaseId+',1668')



##################################################################################################################################


def checkStatusForAllButtons(h,screenInstance,check_count=0,checkButtonStatus=False,rejected=False):

    button_status_for_Import = screenInstance.cm.isButtonEnabled('Import', h)
    button_status_for_Export = screenInstance.cm.isButtonEnabled('Export', h)
    button_status_for_Intersect = screenInstance.cm.isButtonEnabled('Intersect', h)
    button_status_for_Union = screenInstance.cm.isButtonEnabled('Union', h)
    button_status_for_Aut = screenInstance.cm.isButtonEnabled('Aut', h)
    button_status_for_Refersh = screenInstance.cm.isButtonEnabled('Refresh', h)

    if rejected and checkButtonStatus:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Rejected Selection (Import Button always enable)',testcase_id='MKR-1702')
        checkEqualAssert(False,button_status_for_Export,'','','Verify Status of Export Button with Rejected Selection (Export Button enabled on selecting one or more segments from the "Segments" table)',testcase_id='MKR-1706')
        checkEqualAssert(False,button_status_for_Intersect,'','','Verify Status of Intersect Button with Rejected Selection')
        checkEqualAssert(False,button_status_for_Union,'','','Verify Status of Union Button with Rejected Selection')
        checkEqualAssert(False,button_status_for_Aut,'','','Verify Status of Aut Button with Rejected Selection')
        checkEqualAssert(True, button_status_for_Refersh, '', '', 'Verify Status of Refersh Button with Rejected Selection')
        return

    if check_count==0 and checkButtonStatus:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count)+' (Import Button always enable)',testcase_id='MKR-1702')
        checkEqualAssert(False,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count)+' (Export Button enabled on selecting one or more segments from the "Segments" table)',testcase_id='MKR-1706')
        checkEqualAssert(False,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count)+' (Intersect button on Segments page is disabled by default)',testcase_id='MKR-1714')
        checkEqualAssert(False,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count)+' (Union button on Segments page is disabled by default)',testcase_id='MKR-1722')
        checkEqualAssert(False,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count)+' (Aut button on Segments page is disabled by default)',testcase_id='MKR-1730')
        checkEqualAssert(True, button_status_for_Refersh, '', '','Verify Status of Refersh Button with Check_count = ' + str(check_count))
    elif check_count==1 and checkButtonStatus:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count)+' (Import Button always enable)',testcase_id='MKR-1702')
        checkEqualAssert(True,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count)+' (Export Button enabled on selecting one or more segments from the "Segments" table)',testcase_id='MKR-1706')
        checkEqualAssert(False,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count)+ ' (Intersect button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1715')
        checkEqualAssert(False,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count)+' (Union button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1723')
        checkEqualAssert(False,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count)+' (Aut button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1731')
        checkEqualAssert(True, button_status_for_Refersh, '', '','Verify Status of Refersh Button with Check_count = ' + str(check_count))
    elif check_count>1 and checkButtonStatus:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count)+' (Import Button always enable)',testcase_id='MKR-1702')
        checkEqualAssert(True,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count)+' (Export Button enabled on selecting one or more segments from the "Segments" table)',testcase_id='MKR-1706')
        checkEqualAssert(True,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count)+ '(Intersect button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1715')
        checkEqualAssert(True,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count)+' (Union button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1723')
        checkEqualAssert(True,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count)+' (Aut button becomes active on selecting more than one segments from the Segments table)',testcase_id='MKR-1731')
        checkEqualAssert(True, button_status_for_Refersh, '', '','Verify Status of Refersh Button with Check_count = ' + str(check_count))


def createFilterMap(filters,keys):
    return dict(zip(keys,filters))


def buttonStatus(setup,screenInstance):
    button_status = screenInstance.cm.isButtonEnabled(MRXConstants.Apply_Filter,getHandle(setup, MRXConstants.FILTERSCREEN, "allbuttons"))
    checkEqualAssert(True, button_status, '', '', 'Verify Button Status after apply Segment Name Filter')

def checkSlider(screenInstance,h,index=0):
    colorOfEnabled = findPropertyColor(screenInstance, h, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=index)
    if str(colorOfEnabled) != MRXConstants.WHITECOLOR:
        return False
    else:
        return True

def setSlider(screenInstance,h,index=0):
    if not checkSlider(screenInstance,h,index=index):
        try:
            screenInstance.cm.click(h['allsliders']['slider'][index])
            time.sleep(2)
            return checkSlider(screenInstance,h,index=index)
        except:
            logger.debug("Not able to Click on Slider")
            return False


def setFilters(setup,screenInstance,h,k=0):

    selected_filter=[]
    global_filter = setup.cM.getNodeElements("segmentFilter", "filter")
    filter_segmentName = setInputFilter(setup, screenInstance, h, global_filter, 0, 0, 'segmentname', k)
    selected_filter.append(filter_segmentName)

    ##################################### Set User limit#####################################################

    selectedFilter_listforUserlimit = []
    if str(global_filter[str(k)]['user']).split('::')[0]!=' ' or str(global_filter[str(k)]['user']).split('::')[1]!=' ':
        if setSlider(screenInstance,h,1):
            min=str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)]['user']).split('::')[0], h, 1))
            max=str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)]['user']).split('::')[1], h, 2))

            le = u"\u2264"
            ge= u"\u2265"

            if len(min.strip(''))!=0 and len(max.strip(''))!=0:
                selectedFilter_listforUserlimit.append(u"{0}".format(ge)+ min +" and "+u"{0}".format(le)+ max)
            elif len(min.strip(''))!=0:
                selectedFilter_listforUserlimit.append(u"{0}".format(ge) + min)
            elif len(max.strip(''))!=0:
                selectedFilter_listforUserlimit.append(u"{0}".format(le) + max)

        dumpResultForButton(True, "#User", screenInstance, setup, screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
    selected_filter.append(selectedFilter_listforUserlimit)

    ######################################### Set Created On#################################################

    selectedFilter_listforCreatedOn = []
    if str(global_filter[str(k)]['createdon']).split('::')[0]!=' ' and str(global_filter[str(k)]['createdon']).split('::')[1]!=' ':
        if setSlider(screenInstance, h, 2):
            select=screenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(h,indexToBeSelected=int(str(global_filter[str(k)]['createdon']).split('::')[0].strip('')),index=0)
            dumpResultForButton(False, "Created on without Date", screenInstance, setup,screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
            try:
                te = setup.d.execute_script("return document.getElementsByClassName('datePickerIcon')")
                setup.d.execute_script("arguments[0].click()", te[0])
                [year,month,day,hour,min]=str(global_filter[str(k)]['createdon']).split('::')[1].split(' ')
                setCalendar(year, month, day, hour, min, screenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")
                screenInstance.cm.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, "allbuttons"))
                choosedate=screenInstance.cm.getValue_input(h,3)
                selectedFilter_listforCreatedOn.append(str(select) + " " + str(choosedate))
                dumpResultForButton(True, "Created on with Date", screenInstance, setup, screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
            except:
                logger.debug('Not able to click on DatePickerIcon')
                screenInstance.cm.click(h['allsliders']['slider'][2])
                time.sleep(2)
    selected_filter.append(selectedFilter_listforCreatedOn)

    #############################################################################################################

    filter_status = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 3, 0, 'status', 3, k)
    selected_filter.append(filter_status)

    filter_source = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 4, 1, 'source', 6, k)
    selected_filter.append(filter_source)

    filter_owner = setInputFilter(setup, screenInstance, h, global_filter, 5, 4, 'owner', k)
    selected_filter.append(filter_owner)

    filter_access = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 6, 2, 'access', 2, k)
    selected_filter.append(filter_access)

    return selected_filter



def setInputFilter(setup,screenInstance,h,global_filter,index,input_index,tab_name,k=0):
    selectedFilter_list = []
    if str(global_filter[str(k)][tab_name]) != ' ':
        if setSlider(screenInstance, h, int(index)):
            selectedFilter_list.append(str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)][tab_name]), h, input_index)))
            dumpResultForButton(True, tab_name, screenInstance, setup, screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
    return selectedFilter_list


def setMultiDropDownFilter(setup,screenInstance,h,global_filter,index,multi_index,tab_name,max_selection_option,k=0):
    selectedFilter_list = []
    if str(global_filter[str(k)][tab_name]) != ' ':
        if setSlider(screenInstance, h, int(index)):
            status_list = str(global_filter[str(k)][tab_name]).split(',')
            selected_list = screenInstance.picker.domultipleSelectionWithIndex(h, status_list, int(multi_index),parent="allDropDown")
            if len(selected_list) == int(max_selection_option):
                selectedFilter_list.append(MRXConstants.ALL)
            else:
                selectedFilter_list.append(str(' , '.join(selected_list)))

            dumpResultForButton(True,tab_name, screenInstance, setup, screen=MRXConstants.FILTERSCREEN,button_label="Apply Filters")
    return selectedFilter_list




def setSegmentFilter(setup,screenInstance,k='0'):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    Expectedfilter = createFilterMap(setFilters(setup,screenInstance,handle,k=k),Keys)
    return Expectedfilter


def clickOnfilterIcon(setup,screen,filterIcon,parent='filterArea'):
    logger.info("Clicking on FilterIcon")
    h=getHandle(setup,screen,parent)
    try:
        h[parent][filterIcon][0].click()
    except:
        logger.info('Not able to click on = %s',filterIcon)
        resultlogger.info('Not able to click on = %s', filterIcon)
        False
    return True


def getSegmentFilter(setup,screenInstance):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    Expectedfilter = createFilterMap(getFilters(setup,screenInstance,handle),Keys)
    return Expectedfilter


def getFilters(setup,screenInstance,h):

    selected_filter=[]

    filter_segmentName = getInputFilter(screenInstance, h, 0, 0)
    selected_filter.append(filter_segmentName)

#####################################################

    selectedFilter_listforUserlimit = []
    if checkSlider(screenInstance,h,1):
        min=str(screenInstance.cm.getValue_input(h, 1))
        max=str(screenInstance.cm.getValue_input(h, 2))

        le = u"\u2264"
        ge= u"\u2265"

        if len(min.strip(''))!=0 and len(max.strip(''))!=0:
            selectedFilter_listforUserlimit.append(u"{0}".format(ge)+ min +" and "+u"{0}".format(le)+ max)
        elif len(min.strip(''))!=0:
            selectedFilter_listforUserlimit.append(u"{0}".format(ge) + min)
        elif len(max.strip(''))!=0:
            selectedFilter_listforUserlimit.append(u"{0}".format(le) + max)
    selected_filter.append(selectedFilter_listforUserlimit)

#####################################################

    selectedFilter_listforCreatedOn = []
    if checkSlider(screenInstance, h, 2):
        select=screenInstance.dropdown.getSelectionOnVisibleDropDown(h,index=0)
        choosedate=screenInstance.cm.getValue_input(h,3)
        selectedFilter_listforCreatedOn.append(str(select) + " " + str(choosedate))
    selected_filter.append(selectedFilter_listforCreatedOn)

#####################################################

    filter_status = getMultiDropDownFilter(screenInstance, h,3, 0,3)
    selected_filter.append(filter_status)

    filter_source = getMultiDropDownFilter(screenInstance, h,4, 1,6)
    selected_filter.append(filter_source)

    filter_owner = getInputFilter(screenInstance, h,5, 4)
    selected_filter.append(filter_owner)

    filter_access = getMultiDropDownFilter(screenInstance, h,6, 2,2)
    selected_filter.append(filter_access)

    return selected_filter


def getMultiDropDownFilter(screenInstance,h,index,multi_index,max_selection_option):
    selectedFilter_list = []
    if checkSlider(screenInstance, h, int(index)):
        selected_list = screenInstance.picker.getSelection(h,int(multi_index),parent="allDropDown")
        if len(selected_list) == int(max_selection_option):
            selectedFilter_list.append(MRXConstants.ALL)
        else:
            selectedFilter_list.append(str(' , '.join(selected_list)))
    return selectedFilter_list


def getInputFilter(screenInstance,h,index,input_index):
    selectedFilter_list = []
    if checkSlider(screenInstance, h, int(index)):
        selectedFilter_list.append(str(screenInstance.cm.getValue_input(h,input_index)))
    return selectedFilter_list



def getGlobalFiltersFromScreen(screenName,screenInstance, setup,flag=True):
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    actualFilters = insertKeys(screenInstance.globalfilter.getAllSelectedFilters(getHandle(setup,screenName,"filterArea"),flag=flag),Keys)
    return actualFilters


def getGlobalFiltersToolTipData(screenName,filterScreenInstance,setup,flag=True):
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    actualFilters = insertKeys(filterScreenInstance.globalfilter.getToolTipData(setup,getHandle(setup,screenName),screenName=MRXConstants.SEGMENTSCREEN,flag=flag),Keys)
    return actualFilters


def insertKeys(dictionary,keys):
    if type(dictionary) == dict:
        for k in keys:
            if k not in dictionary.keys():
                dictionary[k] = []
        return dictionary
    else:
        return dictionary







def performLogicalOperation(setup,screenInstance,button_label,checkButtonStatus=False):
    check_Count=0
    #tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    segmentScreenHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons')
    checkBoxForLogicalOp = setup.cM.getNodeElements("selectCheckBoxForPerformLogicalOpertion", "segment")
    selectedSegments=[]

    for k, checkboxname in checkBoxForLogicalOp.iteritems():
        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        time.sleep(2)
        index = screenInstance.table.getRowIndexFromTable(0, tableHandle, checkboxname['segmentname'])

        if index != -1:
            screenInstance.cm.clickCheckBox(tableHandle, index, parent="table")
            time.sleep(2)
            if screenInstance.cm.isCheckBoxSelected_MRX(tableHandle, index, parent="table"):
                time.sleep(2)
                if checkboxname['status'] == 'Rejected':
                    checkStatusForAllButtons(segmentScreenHandle, screenInstance, check_Count,checkButtonStatus,rejected=True)
                    screenInstance.cm.clickCheckBox(tableHandle, index, parent="table")
                else:
                    selectedSegments.append(checkboxname['segmentname'])
                    check_Count = check_Count + 1
                    checkStatusForAllButtons(segmentScreenHandle, screenInstance, check_Count,checkButtonStatus)

                    if check_Count > 1:
                        # perform Intersection
                        screenInstance.cm.clickButton(button_label, segmentScreenHandle)
                        import random
                        access = random.choice(['Private', 'Shared'])
                        uniquecountforIntersection = str(5)
                        uniquecountforUnion = str(int(check_Count) * 15 - (int(check_Count) - 1) * 5)
                        uniquecountforAut = str(int(check_Count) * 10)

                        intersectSegmentName = 'autoIntersection_' + str(check_Count)
                        unionSegmentName = 'autoUnion_' + str(check_Count)
                        autSegmentName = 'autoAut_' + str(check_Count)

                        # perform Intersection
                        if button_label=='Intersect':
                            segmentDetailFromUIPopup = logicalOperationSegment(setup, screenInstance,checkboxname,intersectSegmentName, access,uniquecountforIntersection,'Intersection')
                            verifyEntryEditSuccessfully(setup, screenInstance, checkboxname,segmentDetailFromUIPopup, intersectSegmentName,testCaseId='MKR-1672,1719',testCaseId_1='MKR-1716')

                        # perform Union
                        if button_label == 'Union':
                            segmentDetailFromUIPopup = logicalOperationSegment(setup, screenInstance,checkboxname, unionSegmentName,access, uniquecountforUnion,'Union')
                            verifyEntryEditSuccessfully(setup, screenInstance, checkboxname,segmentDetailFromUIPopup, unionSegmentName,testCaseId='MKR-1673,1727',testCaseId_1='MKR-1724')

                        # perform Aut
                        if button_label == 'Aut':
                            segmentDetailFromUIPopup = logicalOperationSegment(setup, screenInstance,checkboxname, autSegmentName,access, uniquecountforAut,'Aut')
                            verifyEntryEditSuccessfully(setup, screenInstance, checkboxname,segmentDetailFromUIPopup, autSegmentName,testCaseId='MKR-1674,1735',testCaseId_1='MKR-1732')

                        screenInstance.cm.clickButton('Refresh', getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
                        time.sleep(3)
                        #tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                        #screenInstance.table.scrollUpTable(tableHandle, driver=setup)
                        if checkboxname['button']!='Cancel':
                            tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
                            for segmentName in selectedSegments:
                                index = screenInstance.table.getRowIndexFromTable(0, tableHandle, str(segmentName))
                                screenInstance.cm.clickCheckBox(tableHandle, index, parent="table")

    screenInstance.cm.clickButton('Refresh', getHandle(setup, MRXConstants.SEGMENTSCREEN, 'allbuttons'))
    time.sleep(3)