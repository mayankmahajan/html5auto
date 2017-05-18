# coding=utf-8
from Utils.utility import *
from classes.Pages.GenerateReportsPopClass import GenerateReportsPopClass
from MRXUtils.MRXConstants import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from classes.Pages.MuralScreens.CheckPrivileges import *


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

def dumpResultForButton(condition,request,screenInstance,setup,button_label="Import"):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, MRXConstants.POPUPSCREEN,"allbuttons"))
    checkEqualAssert(condition,button_status,"","","Checking State of "+button_label+" for Fields entered : "+str(request))
    return button_status

def VerifyBasicTableFuncationality(setup,screenInstance,parent='table'):
    columns = setup.cM.getNodeElements("segmentsorttablecolumn", "column")
    column_names = []
    for k, column in columns.iteritems():
        column_names.append(column['locatorText'])

    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, parent)
    tableMap = screenInstance.table.getTableDataMap(tableHandle,driver=setup,colIndex=-1)

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

    checkEqualAssert(sorted(col, reverse=True), col, "", "", "Checking ColumnName Sort : " + columnName)
    logger.info("Sorted")
    cdata2 = insatnce.table.convertDataToDictWithKeyAsRow(data2)
    return cdata2


def set_GetDetailFromEdit(setup,screenInstance,isSetEdit,segment_Input):
    popUpDetails=[]

    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    if segment_Input['edit_info']=='edit':
        checkEqualAssert(MRXConstants.EDITHEADERINEDITPOPUP,str(popUpHandle['allspans']['span'][0].text),'','','Verify Edit Header in Popup')
    elif segment_Input['edit_info']=='info':
        checkEqualAssert(MRXConstants.EDITHEADERINEDITPOPUP, str(popUpHandle['allspans']['span'][0].text), '', '','Verify Info Header in Popup')
    #popUpDetails[str(popUpHandle['allspans']['span'][1].text).strip(':')]=str(popUpHandle['allspans']['span'][2].text)
    #popUpDetails[str(popUpHandle['allspans']['span'][3].text).strip(':')] = str(popUpHandle['allspans']['span'][4].text)
    import re
    #popUpDetails['#Users'] = re.findall('[0-9]*',str(popUpHandle['allspans']['span'][5].text))[0]

    if isSetEdit and segment_Input['edit_info']=='edit':
        #popUpDetails['Segment Name']=screenInstance.cm.sendkeys_input(segment_name,popUpHandle,0)
        popUpDetails.append(screenInstance.cm.sendkeys_input(segment_Input['newsegmentname'], popUpHandle, 0))
        popUpDetails.append(re.findall('[0-9]*',str(popUpHandle['allspans']['span'][5].text))[0])
        popUpDetails.append(str(popUpHandle['allspans']['span'][2].text))

        if screenInstance.cm.selectRadioButton(segment_Input['access'],popUpHandle,childDiv="label"):
            #popUpDetails['Access'] =str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input"))
            popUpDetails.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))
        else:
            #popUpDetails['Access'] ='Not able to Click Radio Button'
            popUpDetails.append('Not able to Click Radio Button')

    elif segment_Input['edit_info']=='info':
        popUpDetails.append(str(popUpHandle['allspans']['span'][6].text))
        popUpDetails.append('0')
        popUpDetails.append(str(popUpHandle['allspans']['span'][2].text))
        popUpDetails.append(str(popUpHandle['allspans']['span'][8].text))
    else:
        #popUpDetails['Segment Name'] = str(screenInstance.cm.getValue_input(popUpHandle, 0))
        #popUpDetails['Access'] = str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input"))
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
        # isError(setup)
        logger.info("********Folowing Updated Data added into table =%s ************", popUpDetails)
        return popUpDetails



def importSegment(setup,screenInstance,segment_Input,source='Import'):

    flag_segmentname = False
    flag_filepath = False
    segmentDetailFromUI=[]
    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    checkEqualAssert(MRXConstants.IMPORTSEGMENT, str(popUpHandle['allspans']['span'][0].text), '', '','Verify Import Segment Header in Import Popup')

    logger.info('Going to Enter Segment Name = %s',segment_Input['segmentname'])
    resultlogger.info('Going to Enter Segment Name = %s',segment_Input['segmentname'])
    #segmentDetailFromUI['Segment Name'] = str(screenInstance.cm.sendkeys_input(segment_Input['segmentname'],popUpHandle,0))
    segmentDetailFromUI.append(str(screenInstance.cm.sendkeys_input(segment_Input['segmentname'],popUpHandle,0)))

    # if not isColorValid(screenInstance, popUpHandle,property=Constants.BORDERCOLOR, index=0):
    #     raise
    flag_segmentname=True
    dumpResultForButton(flag_segmentname and flag_filepath, "Segment Name", screenInstance,setup)

    if segment_Input['status']=='Completed':
        segmentDetailFromUI.append('14')
    else:
        segmentDetailFromUI.append('0')

    segmentDetailFromUI.append(segment_Input['status'])
    segmentDetailFromUI.append(source)
    segmentDetailFromUI.append(Constants.USERNAME)
    #segmentDetailFromUI['Source']='Import'
    #segmentDetailFromUI['#User'] = '14'
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
    popUpHandle['browsebuttons']['browsebutton'][0].find_elements_by_xpath('./*/*')[0].send_keys(segment_Input['file'])

    checkEqualAssert(False,'No File' in str(popUpHandle['footerText']['text'][0].text),'','',"Verify File Selected from Path  => " + segment_Input['file'])
    flag_filepath=not 'No File' in str(popUpHandle['footerText']['text'][0].text)
    button_status=dumpResultForButton(flag_segmentname and flag_filepath, "Select .CSV File", screenInstance,setup)

    import datetime
    #now = datetime.datetime.now()
    utc = datetime.datetime.utcnow()
    dateString=utc.strftime("%Y-%m-%d %H:%M")

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



def checkStatusForAllButtons(h,screenInstance,check_count=0):

    button_status_for_Import = screenInstance.cm.isButtonEnabled('Import', h)
    button_status_for_Export = screenInstance.cm.isButtonEnabled('Export', h)
    button_status_for_Intersect = screenInstance.cm.isButtonEnabled('Intersect', h)
    button_status_for_Union = screenInstance.cm.isButtonEnabled('Union', h)
    button_status_for_Aut = screenInstance.cm.isButtonEnabled('Aut', h)

    if check_count==0:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count))
    elif check_count==1:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count))
        checkEqualAssert(True,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count))
        checkEqualAssert(False,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count))
    elif check_count>1:
        checkEqualAssert(True,button_status_for_Import,'','','Verify Status of Import Button with Check_count = '+str(check_count))
        checkEqualAssert(True,button_status_for_Export,'','','Verify Status of Export Button with Check_count = '+str(check_count))
        checkEqualAssert(True,button_status_for_Intersect,'','','Verify Status of Intersect Button with Check_count = '+str(check_count))
        checkEqualAssert(True,button_status_for_Union,'','','Verify Status of Union Button with Check_count = '+str(check_count))
        checkEqualAssert(True,button_status_for_Aut,'','','Verify Status of Aut Button with Check_count = '+str(check_count))



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

    filter_segmentName=[]
    filter_user=[]
    filter_createdon = []
    filter_status=[]
    filter_source=[]
    filter_access=[]
    filter_owner=[]

    global_filter = setup.cM.getNodeElements("segmentFilter", "filter")
    filter_segmentName = setInputFilter(setup, screenInstance, h, global_filter, 0, 0, 'segmentname', k)

    # Set User limit

    if str(global_filter[str(k)]['user']).split('::')[0]!=' ' or str(global_filter[str(k)]['user']).split('::')[1]!=' ':
        if setSlider(screenInstance,h,1):
            min=str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)]['user']).split('::')[0], h, 1))
            max=str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)]['user']).split('::')[1], h, 2))

            if len(min.strip(''))!=0 and len(max.strip(''))!=0:
                filter_user.append('≥'+min+" and "+'≤'+max)
            elif len(min.strip(''))!=0:
                filter_user.append('≥' + min)
            elif len(max.strip(''))!=0:
                filter_user.append('≤' + max)

        dumpResultForButton(True, "#User", screenInstance, setup, button_label="Apply Filters")

    # Set Created On

    if str(global_filter[str(k)]['createdon']).split('::')[0]!=' ' and str(global_filter[str(k)]['createdon']).split('::')[1]!=' ':
        if setSlider(screenInstance, h, 2):
            select=screenInstance.dropdown.doSelectionOnVisibleDropDownByIndex(h,indexToBeSelected=int(str(global_filter[str(k)]['createdon']).split('::')[0].strip('')),index=0)
            dumpResultForButton(False, "Created on without Date", screenInstance, setup, button_label="Apply Filters")
            try:
                #h['icons']['datePickerIcon'][0].click()
                [year,month,day,hour,min]=str(global_filter[str(k)]['createdon']).split('::')[1].split(' ')
                setCalendar(year, month, day, hour, min, screenInstance, setup, page=Constants.CALENDERPOPUP, parent="leftcalendar")
                screenInstance.cm.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, "allbuttons"))
                choosedate=screenInstance.cm.getValue_input(h,3)
                filter_createdon.append(str(select) + " " + str(choosedate))
            except:
                logger.debug('Not able to click on DatePickerIcon')
        dumpResultForButton(True, "Created on with Date", screenInstance, setup, button_label="Apply Filters")


    filter_status = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 3, 0, 'status', 2, k)
    filter_source = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 4, 1, 'source', 6, k)
    filter_owner = setInputFilter(setup, screenInstance, h, global_filter, 5, 4, 'owner', k)
    filter_access = setMultiDropDownFilter(setup, screenInstance, h, global_filter, 6, 2, 'access', 2, k)

    return [filter_segmentName,filter_user,filter_createdon,filter_status,filter_source,filter_access,filter_owner]



def setInputFilter(setup,screenInstance,h,global_filter,index,input_index,tab_name,k=0):
    if str(global_filter[str(k)][tab_name]) != ' ':
        selectedFilter_list=[]
        if setSlider(screenInstance, h, int(index)):
            selectedFilter_list.append(str(screenInstance.cm.sendkeys_input(str(global_filter[str(k)][tab_name]), h, input_index)))
        dumpResultForButton(True, tab_name, screenInstance, setup, button_label="Apply Filters")



def setMultiDropDownFilter(setup,screenInstance,h,global_filter,index,multi_index,tab_name,max_selection_option,k=0):
    if str(global_filter[str(k)][tab_name]) != ' ':
        selectedFilter_list=[]
        if setSlider(screenInstance, h, int(index)):
            status_list = str(global_filter[str(k)][tab_name]).split(',')
            selected_list = screenInstance.picker.domultipleSelectionWithIndex(h, status_list, int(multi_index),parent="allDropDown")
            if len(selected_list) == int(max_selection_option):
                selectedFilter_list.append('ALL')
            else:
                selectedFilter_list.append(str(','.join(selected_list)))

        dumpResultForButton(True,tab_name, screenInstance, setup, button_label="Apply Filters")
        return selectedFilter_list




def setSegmentFilter(setup,screenInstance,k='0'):
    Expectedfilter=[]
    handle=getHandle(setup,MRXConstants.FILTERSCREEN)
    Keys = setup.cM.getAllNodeElements("segment_Filters", "filter")
    Expectedfilter = createFilterMap(setFilters(setup,screenInstance,handle,k=k),Keys)
    return Expectedfilter


def clickOnfilterIcon(setup,screen):
    logger.info("Clicking on FilterIcon")
    h=getHandle(setup,screen,"filterArea")
    h['filterArea']['filterIcon'][0].click()
    return True



def getGlobalFiltersFromScreen(screenName,globalFilterInstance, setup):

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