from Utils.utility import *
from MRXConstants import *
from classes.Components.TimeRangeComponentClass import *
from MRXUtils import SegmentHelper
import datetime

Delimiter=' , '

def button_Status(condition,request,screenInstance,setup,screen=MRXConstants.POPUPSCREEN,button_label="Create",testcase_id=''):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, screen,"allbuttons"))
    checkEqualAssert(condition,button_status,message="Checking State of "+button_label+ " button ::" +request,testcase_id=testcase_id)
    return button_status


def setGlobalFilters(udpScreenInstance,setup,k='0'):
    segmentKeys=setup.cM.getAllNodeElements("segmenntFilters","filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters","filter")
    networkKeys = setup.cM.getAllNodeElements("networkFilters","filter")
    contentKeys = setup.cM.getAllNodeElements("contentFilters","filter")
    usageKeys = setup.cM.getAllNodeElements("usageFilters","filter")

    segmentFilters = createFilterMap(setFilters(setup,udpScreenInstance,"segment",k=k),segmentKeys)
    deviceFilters = createFilterMap(setFilters(setup,udpScreenInstance,"device",k=k),deviceKeys)
    networkFilters = createFilterMap(setFilters(setup,udpScreenInstance,"network",k=k),networkKeys)
    contentFilters = createFilterMap(setFilters(setup,udpScreenInstance,"content",k=k),contentKeys)
    usageFilters = createFilterMap(setFilters(setup,udpScreenInstance,"usage",k=k),usageKeys)

    expectedFilters = merge_dictionaries(merge_dictionaries(merge_dictionaries(merge_dictionaries(segmentFilters,deviceFilters),networkFilters),contentFilters),usageFilters)
    logger.info('Selected filter are =%s',expectedFilters)
    resultlogger.info('Selected filter are =%s',expectedFilters)
    return expectedFilters

def createFilterMap(filters,keys):
    return dict(zip(keys,filters))

def parseFilters(global_filter):
    filters = {}
    for id in global_filter.keys():
        filters[id] = parseFilter(id,global_filter)
    return filters

def parseFilter(id,global_filter):
    flist = []
    for f in global_filter[str(id)]['filters'].split("::"):
        flist.append(str(f).split(','))
    return flist

def setQuickLink_Measure(setup,udScreenInstance,i='0'):
    quicklink = setup.cM.getNodeElements("udpScreenFilters", 'quicklink')
    measure = setup.cM.getNodeElements("udpScreenFilters", 'measure')
    if quicklink[str(i)]['locatorText'] == 'CustomClick':
        selectedQuicklink=quicklink[str(i)]['locatorText']
        calHandler = getHandle(setup, MRXConstants.UDPPOPUP, "ktrs")
        logger.info("Launching Calendar from UDP Popup")
        calHandler['ktrs']['datepicker'][0].click()
        logger.info("Calendar picker is clicked")

        [year, month, day, hour, min] = str(quicklink[str(i)]['startTime']).split(' ')
        setCalendar(year, month, day, hour, min, udScreenInstance, setup, page=Constants.CALENDERPOPUP,parent="leftcalendar")

        [et_year, et_month, et_day, et_hour, et_min] = str(quicklink[str(i)]['endTime']).split(' ')
        setCalendar(et_year, et_month, et_day, et_hour, et_min, udScreenInstance, setup,Constants.CALENDERPOPUP, "rightcalendar")

        valueFromCalender=str(getHandle(setup,Constants.CALENDERPOPUP,'allspans')['allspans']['span'][0].text).strip()
        # Closing Calendar Pop Up
        udScreenInstance.clickButton("Apply",getHandle(setup, Constants.CALENDERPOPUP, Constants.ALLBUTTONS))
        logger.info("Calendar Selection done at Filter Popup = %s ", valueFromCalender)
        t1 = udScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
        checkEqualAssert(valueFromCalender, t1, selectedQuicklink, "", "verify quicklink label")

    else:
        udScreenInstance.timeBar.setQuickLink(quicklink[str(i)]['locatorText'], getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
        isError(setup)
        selectedQuicklink = udScreenInstance.timeBar.getSelectedQuickLink(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
        t = TimeRangeComponentClass().get_Label(str(quicklink[str(i)]['locatorText']).lower())
        t1 = udScreenInstance.timeBar.getLabel(getHandle(setup, MRXConstants.UDPPOPUP, "ktrs"))
        checkEqualAssert(t[1], t1, selectedQuicklink, "", "verify quicklink label")

    selectedMeasure = udScreenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MRXConstants.UDPPOPUP, "allselects"), str(measure[str(i)]['locatorText']), index=0, parent="allselects")
    if quicklink[str(i)]['locatorText']!='CustomClick':
        timeRangeFromPopup=str(t1+" ("+selectedQuicklink.strip()+")").strip()
    else:
        timeRangeFromPopup = str(t1)
    measureFromPopup=str(selectedMeasure).strip()

    return timeRangeFromPopup,measureFromPopup




def setFilters(setup,udpScreenInstance,tab_name,k ="0"):
    udp_filter= parseFilters(setup.cM.getNodeElements("udpScreenFilters",tab_name))
    udpfilters= setup.cM.getNodeElements("udpfilters","filter")
    udpScreenInstance.clickLink(udpfilters[tab_name]['locatorText'],getHandle(setup,MRXConstants.UDPPOPUP,MRXConstants.ALLLINKS))

    filterSelected = []
    treeindex=0
    inputFieldIndex=0

    for i in range(len(udp_filter[k])):
        if len(udp_filter[k][i]) == 1 and udp_filter[k][i][0] == ' ':
            filterSelected.append([])
            pass

        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'Do_Selection_On_Tree':
            treeHandle=getHandle(setup,MRXConstants.UDPPOPUP,'alltrees')
            udpScreenInstance.tree.expandTree(treeHandle, index=treeindex)
            level_Dict = udpScreenInstance.tree.seprateElementOfTreeByLevel(treeHandle, index=treeindex)
            expectedFromUI, expected, selected = udpScreenInstance.tree.doSelectionOnTree_Random(setup, level_Dict,treeHandle, index=treeindex)
            checkEqualDict(expected,selected,message='Verify selection on Tree',doSortingBeforeCheck=True)
            treeindex=treeindex+1
            if expectedFromUI != ['']:
                filterSelected.append([expectedFromUI])
            else:
                filterSelected.append([])

        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'No_Selection_On_Tree':
            filterSelected.append([])
            treeindex=treeindex+1

        elif len(udp_filter[k][i]) ==1 and udp_filter[k][i][0] == 'Input':
            input_value=setup.cM.getNodeElements("udpScreenFilters",tab_name)[k]['inputvalue']
            inputvalue=str(udpScreenInstance.cm.sendkeys_input(input_value, getHandle(setup,MRXConstants.UDPPOPUP,'allinputs'), inputFieldIndex))
            filterSelected.append(inputvalue.split(','))
            inputFieldIndex=inputFieldIndex+1

        elif len(udp_filter[k][i]) == 1 and udp_filter[k][i][0] == 'No_Input':
            filterSelected.append([])
            inputFieldIndex = inputFieldIndex + 1

        else:
            equalOrNotEqual=udpScreenInstance.multiDropdown.setEqualOrNotEqualIcon(getHandle(setup,MRXConstants.UDPPOPUP,"filterPopup"),udp_filter[k][i],(i-treeindex-inputFieldIndex))

            if 'E' in udp_filter[k][i]:
                checkEqualAssert('Equal',str(equalOrNotEqual),message='Verify selection For equalSign')
            elif 'NE' in udp_filter[k][i]:
                checkEqualAssert('Not Equal', str(equalOrNotEqual),message='Verify selection For equalSign')

            selected  = udpScreenInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,MRXConstants.UDPPOPUP,"filterPopup"),udp_filter[k][i],(i-treeindex-inputFieldIndex))
            if selected != ['']:
                filterSelected.append(selected)
            else:
                filterSelected.append([])

    return filterSelected


def getUDPFiltersToolTipData(screenName,setup):
    segmentKeys = setup.cM.getAllNodeElements("segmenntFilters", "filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters", "filter")
    networkKeys = setup.cM.getAllNodeElements("networkFilters", "filter")
    contentKeys = setup.cM.getAllNodeElements("contentFilters", "filter")
    usageKeys = setup.cM.getAllNodeElements("usageFilters", "filter")


    actualFilters = insertKeys(getToolTipData(setup,getHandle(setup,screenName)),segmentKeys+deviceKeys+networkKeys+contentKeys+usageKeys)
    return actualFilters


def insertKeys(dictionary,keys):
    if type(dictionary) == dict:
        for k in keys:
            if k not in dictionary.keys():
                dictionary[k] = []
        return dictionary
    else:
        return dictionary


def getToolTipData(setup,h,parent="filterArea",tooltip_parent = "globalfiltertooltip",child="filterText",screenName=MRXConstants.UDPPOPUP,flag=True):
    try:
        logger.info("Performing Hover action on UDP Filter text Area")
        setup.dH.action.move_to_element(h[parent][child][0]).perform()
        tooltipHandle = getHandle(setup,screenName,tooltip_parent)
        filters = getAllSelectedFilters(tooltipHandle,tooltip_parent,child,flag=flag)
        logger.info("Got Tooltip data = %s",str(filters))
        return filters
    except Exception as e:
        logger.error("Got Exception while getting tooltip data for Global Filters = %s",str(e))
        return e


def getAllSelectedFilters(h,parent="filterArea",child="filterText",flag=True):
    filters = {}
    try:
        if not h[parent][child]:
            filters = str(h[parent]['filter'][0].text)
            logger.info("Got Selected Filters as %s",filters)
        else:
            for ele in h[parent][child]:
                # sleep(2)
                if str(ele.text)!='':
                    if flag==True:
                        temp = []
                        # ele.send_keys(Keys.NULL)
                        uifilter = str(ele.text).split(':')
                        if '>' in uifilter[1]:
                            filters[uifilter[0].strip()]=[str(uifilter[1]).strip()]
                        else:
                            for s in uifilter[1].split(Delimiter):
                                temp.append(s.strip())
                            filters[uifilter[0].strip()] = temp
                            # sleep(2)

                    else:
                        #for handling : and , for MRX Segment filter
                        key_value=(ele.text).split(':', 1)
                        try:
                            filters[str(key_value[0]).strip()] = [str(key_value[1]).strip()]
                        except Exception as e:
                            filters[str(key_value[0]).strip()] = [key_value[1].strip()]
                # sleep(2)
        return filters
    except Exception as e:
        return e


def getUDPFiltersFromScreen(screenName,setup):
    segmentKeys = setup.cM.getAllNodeElements("segmenntFilters", "filter")
    deviceKeys = setup.cM.getAllNodeElements("deviceFilters", "filter")
    networkKeys = setup.cM.getAllNodeElements("networkFilters", "filter")
    contentKeys = setup.cM.getAllNodeElements("contentFilters", "filter")
    usageKeys = setup.cM.getAllNodeElements("usageFilters", "filter")

    actualFilters = insertKeys(getAllSelectedFilters(getHandle(setup,screenName,"filterArea")),segmentKeys+deviceKeys+networkKeys+contentKeys+usageKeys)
    return actualFilters

def verifySummary(screenInstance,data,h,parent='alllabels',child='label'):
    summaryTextLine1=str(h[parent][child][0].text)
    summaryTextLine2 = str(h[parent][child][1].text)

    numberofUsersFromSummary=UnitSystem().convertStringToExactInteger(summaryTextLine1.split('Subscribers')[0].strip())
    percentageOfVolumeFromSummary=int(summaryTextLine1.split('/')[1].split('%')[0].strip())
    avgVolumePerUserFromSummary=summaryTextLine2.split('er:')[1]
#################################################################
    user_list = []

    for rows in data['rows']:
        user_list.append(UnitSystem().convertStringToExactInteger(rows[1]))
    numberofUsersFromTable=sum(user_list)

##################################################################
    perVolume_list=[]
    for rows in data['rows']:
        if '<' in (rows[2]):
            perVolume_list.append(0.0)
        else:
            perVolume_list.append(float(rows[2]))

    percentageOfVolumeFromTable=int(round(sum(perVolume_list)))
##################################################################
    Avg_Volume = []
    for rows in data['rows']:
        Avg_Volume.append(rows[4].strip())

    raw_value=screenInstance.table.getValueFromTable(Avg_Volume,'avg')
    avgVolumePerUserFromTable=UnitSystem().getValueFromRawValue(raw_value, unitValue=1024)

    checkEqualAssert(percentageOfVolumeFromTable,percentageOfVolumeFromSummary,message='Verify % of volume on Summary with selected Table')
    checkEqualAssert(numberofUsersFromTable,numberofUsersFromSummary,message='Verify % of volume on Summary with selected Table')
    checkEqualAssert(avgVolumePerUserFromTable,avgVolumePerUserFromSummary.strip(),message='Verify Avg Volume on Summary with selected Table')

    return [summaryTextLine1,summaryTextLine2]


def createSegmentFromUD(setup,screenInstance,segment_Input):
    popUpDetails=[]
    key_Class='titleSpan'
    value_Class='titleValueSpan'
    popUpHandle = getHandle(setup, MRXConstants.POPUPSCREEN)
    checkEqualAssert(MRXConstants.CREATESEGMENT, str(popUpHandle['allspans']['span'][0].text),'Verify Create Segment Header in Popup')

    ##############################################################################
    key_list=[]
    value_list=[]
    for span in popUpHandle['allspans']['span']:
        if span.get_attribute('class') == key_Class and len(key_list)<5:
            key_list.append(str(span.text))
        elif span.get_attribute('class') == value_Class and len(value_list)<5:
            value_list.append(str(span.text))
        if len(key_list)==4 and len(value_list)==4:
            break

    if len(key_list)==len(value_list):
        detailFromUI_Dict={}
        for i in range(len(key_list)):
            detailFromUI_Dict[key_list[i]]=value_list[i]

    ##############################################################################

    button_Status(False,"Without Entering Segment Name",screenInstance,setup)
    button_Status(True,"Without Entering Segment Name",screenInstance,setup,button_label='Cancel')

    popUpDetails.append(screenInstance.cm.sendkeys_input(segment_Input['segmentname'], popUpHandle, 0))
    button_status=button_Status(True,"After Entering Segment Name",screenInstance,setup)
    cancel_button_status=button_Status(True,"After Entering Segment Name",screenInstance,setup,button_label='Cancel')

    popUpDetails.append(str(popUpHandle['allspans']['span'][len(popUpHandle['allspans']['span']) - 4].text).split('Subscribers')[0].strip())

    line1=str(popUpHandle['allspans']['span'][len(popUpHandle['allspans']['span']) - 4].text)
    line2=str(popUpHandle['allspans']['span'][len(popUpHandle['allspans']['span']) - 3].text)

    textFromPopUp=[line1,line2]

    if MRXConstants.MinimumUserConfig > UnitSystem().convertStringToExactInteger(str(popUpHandle['allspans']['span'][len(popUpHandle['allspans']['span']) - 4].text).split('Subscribers')[0].strip()):
        popUpDetails.append('Rejected')
    else:
        popUpDetails.append(segment_Input['status'])

    popUpDetails.append(MRXConstants.Source_User_Distribution)
    popUpDetails.append('admin')

    logger.info('Going to Enter Access = %s', segment_Input['access'])
    resultlogger.info('Going to Enter Access = %s', segment_Input['access'])

    if screenInstance.cm.selectRadioButton(segment_Input['access'], popUpHandle, childDiv="label"):
        popUpDetails.append(str(screenInstance.cm.getSelectedRadioButtonText(popUpHandle, childDiv="input")))
    else:
        popUpDetails.append('Not Able to Click on Radio Button')

    utc = datetime.datetime.utcnow()
    dateString = utc.strftime(MRXConstants.TIMEPATTERN)
    popUpDetails.append(str(dateString))

    if segment_Input['button'] == 'Create' and button_status:
        logger.info('Going to Click on %s Button ', segment_Input['button'])
        click_status = screenInstance.cm.clickButton(str(segment_Input['button']), popUpHandle)
        checkEqualAssert(True, click_status, "", "","Verify whether " + segment_Input['button'] + " button clicked or not")
        logger.info("********Folowing Updated Data added into table =%s ************", popUpDetails)
        return popUpDetails,detailFromUI_Dict,textFromPopUp

    elif segment_Input['button'] == 'Cancel' and cancel_button_status:
        logger.info('Going to Click on %s Button ', segment_Input['button'])
        click_status = screenInstance.cm.clickButton(str(segment_Input['button']), popUpHandle)
        checkEqualAssert(True, click_status, "", "","Verify whether " + segment_Input['button'] + " button clicked or not")
        return [],detailFromUI_Dict,textFromPopUp

    else:
        return [], detailFromUI_Dict, textFromPopUp


def saveNewFilter(setup,screenName,screenInstance,filterDetail,isEdit=False):

    h=getHandle(setup,screenName)
    if isEdit:
        checkEqualAssert("Rename Save Filter", h['allspans']['span'][0].text, message='Verify Rename Save Filter Header')
    else:
        checkEqualAssert("Save New Filter",h['allspans']['span'][0].text,message='Verify Save New Filter Header')
        button_Status(False,"Without Entering filter name",screenInstance,setup,screen=screenName,button_label='Save')
        button_Status(True,"Without Entering filter name",screenInstance,setup,screen=screenName,button_label='Cancel')

    logger.info('Going to enter filter name =%s',str(filterDetail['filtername']))
    filter_name=str(screenInstance.cm.sendkeys_input(str(filterDetail['filtername']), h, 0))

    saveButtonStatus_AfterEnterFilterName=button_Status(True,"After Enter filter name",screenInstance,setup,screen=screenName,button_label='Save')
    cancelButtonStatus_AfterEnterFilterName=button_Status(True,"After Enter filter name",screenInstance,setup,screen=screenName,button_label='Cancel')

    logger.info('Going to set checkbox for Default filter')
    checkBox_Status=screenInstance.cm.isCheckBoxSelected_UMMural(h,0)
    if (checkBox_Status=='1' and filterDetail['default']=='0') or (checkBox_Status==0 and filterDetail['default']=='1'):
        logger.info('Going to set checkbox for Default filter')
        screenInstance.cm.clickCheckBox(h,0)

    if filterDetail['button'] == 'Save' and saveButtonStatus_AfterEnterFilterName :
        logger.info('Going to Click on %s Button ', filterDetail['button'])
        checkBox_Value=screenInstance.cm.isCheckBoxSelected_UMMural(h,0)
        click_status = screenInstance.cm.clickButton(str(filterDetail['button']),h)
        flag=isOverwrite(setup,screenInstance,filterDetail)
        if flag:
            h = getHandle(setup, screenName)
            filterDetail['filtername']=filterDetail['filtername']+'_new'
            filter_name = str(screenInstance.cm.sendkeys_input(str(filterDetail['filtername']), h, 0))
            click_status = screenInstance.cm.clickButton(str(filterDetail['button']),h)

        checkEqualAssert(True, click_status, "", "","Verify whether " + filterDetail['button'] + " button clicked or not")
        logger.info('New Added/Edit Filter Details (Name and default status) = %s',[filter_name,str(checkBox_Value)])
        resultlogger.info('New Added/Edit Filter Details (Name and default status) = %s',[filter_name,str(checkBox_Value)])
        return [filter_name,str(checkBox_Value)]

    elif filterDetail['button'] == 'Cancel' and cancelButtonStatus_AfterEnterFilterName:
        logger.info('Going to Click on %s Button ', filterDetail['button'])
        click_status = screenInstance.cm.clickButton(str(filterDetail['button']), h)
        checkEqualAssert(True, click_status, "", "","Verify whether " + filterDetail['button'] + " button clicked or not")
        return ''

    else:
        try:
            h['icons']['closePopupIcon'][0].click()
        except:
            try:
                h['icons']['closePopupIcon'][0].click()
            except:
                pass

        return ''


def getLoadFilterList(h,parent="loadfilterlist",child="list"):
    logger.info('Going to find loaded filter list')
    filterDict={}
    for ele in h[parent][child]:
        if len(str(ele.text).split('\n'))==1:
            filterDict[str(ele.text).split('\n')[0]]=[str(ele.text).split('\n')[0],'']
        else:
            filterDict[str(ele.text).split('\n')[1]] = [str(ele.text).split('\n')[1],str(ele.text).split('\n')[0]]
    logger.info('loaded filter list =%s',str(filterDict))
    return filterDict

def loadFilter(h,value,parent='loadfilterlist',child='list'):
    try:
        for ele in h[parent][child]:
            if value in str(ele.text).split('\n'):
                ele.click()
                return True
    except:
        logger.error('Not able click on save filter')
        return False

    return False


def verifySaveFilterFromLoadFilter(setup,screenInstance,screenName,filterDetail):
    h=getHandle(setup,screenName)
    checkEqualAssert("Load Filter",h['allspans']['span'][0].text,message='Verify Load Filter Header')
    button_Status(True,"Always Enabled",screenInstance,setup,screen=MRXConstants.UDPPOPUP,button_label='Cancel')
    filter_dict=getLoadFilterList(h)
    screenInstance.clickButton("Cancel", getHandle(setup,screenName,Constants.ALLBUTTONS))
    if filterDetail['button']=="Save":
        expected_Detail=[filterDetail['filtername'],'*' if filterDetail['default']=='1' else '']
        checkEqualAssert(True,filter_dict.has_key(filterDetail['filtername']),message='Filter save successfully :: Filter Detail ='+str(filter_dict[filterDetail['filtername']]))
        checkEqualAssert(expected_Detail,filter_dict[filterDetail['filtername']],message='Verify Detail of new added filter')
    else:
        checkEqualAssert(False, filter_dict.has_key(filterDetail['filtername']),message='Verify that if we Press Cancel or cross (X) then Filter not save')
    return


def loadFilterFormSaveFilter(setup,screenName,filterDetail):
    if filterDetail['button']=='Save':
        h=getHandle(setup,screenName,'loadfilterlist')
        loadFilter(h,filterDetail['filtername'])
    else:
        return False


def checkDefaultFilter(setup,screenInstance,screenName,exploreScreen,filterDetail,expected_filter,timeRangeFromPopup,measureFromPopup):
    if filterDetail['default']=='1':
        exploreHandle = getHandle(setup,exploreScreen)
        if len(exploreHandle['appHeader']['alllinks']) > 0:
            screenInstance.explore.exploreList.clickOnLinkByValue(exploreHandle, Constants.USERNAME)
            exploreHandle = getHandle(setup, exploreScreen)
            screenInstance.explore.exploreList.clickOnLinkByValue(exploreHandle, MRXConstants.Logout)
            time.sleep(5)
            login(setup, Constants.USERNAME, Constants.PASSWORD)
            exploreHandle = getHandle(setup, exploreScreen)
            screenInstance.explore.exploreList.launchModule(exploreHandle, "USER DISTRIBUTION")
            screenHandle = getHandle(setup, screenName, 'time_measure')
            timeRangeFromScreen = str(screenHandle['time_measure']['span'][0].text).strip()
            measureFromScreen = str(screenHandle['time_measure']['span'][1].text).strip()
            udpFilterFromScreen = getUDPFiltersFromScreen(MRXConstants.UDSCREEN, setup)
            checkEqualAssert(timeRangeFromPopup,timeRangeFromScreen,message='Verify timeRange For default loaded filter')
            checkEqualAssert(measureFromPopup,measureFromScreen,message='Verify measuer For default loaded filter')
            checkEqualDict(expected_filter,udpFilterFromScreen, message="Verify Filters for default loaded filter", doSortingBeforeCheck=True)


def clearFilter(setup,screenName,parent='filterArea',child='filterClearIcon'):
    if len(getHandle(setup,screenName,parent)[parent][child]) > 0:
        SegmentHelper.clickOnfilterIcon(setup, screenName,child)
        time.sleep(3)

def isOverwrite(setup,screenInstance,filterDetail):
    handle=getHandle(setup,MRXConstants.SNFPOPUP)
    if str(handle['allspans']['span'][0].text)=='Overwrite?':
        logger.info('Get Popup for Confirm Overwrite')
        alertmsg=str(handle['alertMsg']['msg'][0].text)
        expectedMsg="A saved set of parameters with the same name already exists. Do you want to replace it."
        checkEqualAssert(expectedMsg,alertmsg,message='Verify Overwrite msg')
        if filterDetail['isOverwrite'] == 'True':
            screenInstance.clickButton("OK", getHandle(setup, MRXConstants.SNFPOPUP, Constants.ALLBUTTONS))
            return False
        else:
            try:
                handle['icons']['closePopupIcon'][0].click()
            except:
                try:
                    handle['icons']['closePopupIcon'][0].click()
                except:
                    pass

            return True
    else:
        return False

def deleteSaveFilter(setup,screenName,screenInstance,filterDetail,parent='loadfilterlist',child='list'):
    try:
        h=getHandle(setup,screenName,parent)
        for ele in h[parent][child]:
            if filterDetail['filtername'] in str(ele.text).split('\n'):
                setup.dH.action.move_to_element(ele).perform()
                time.sleep(2)
                ele.find_element_by_class_name('deleteBtn').click()
                flag=confirmDelete(setup,screenInstance,filterDetail)
                filter_dict = getLoadFilterList(getHandle(setup, screenName, parent))
                if flag:
                    checkEqualAssert(False,filter_dict.has_key(filterDetail['filtername']),message='Verify filter delete successfully')
                else:
                    checkEqualAssert(True, filter_dict.has_key(filterDetail['filtername']),message='Verify filter not deleted if press Cancel')
                return
    except:
        logger.error('Not able click on delete button')
        return


def editSaveFilter(setup,screenName,screenInstance,filterDetail,parent='loadfilterlist',child='list'):
    try:
        h=getHandle(setup,screenName,parent)
        for ele in h[parent][child]:
            if filterDetail['filtername'] in str(ele.text).split('\n'):
                setup.dH.action.move_to_element(ele).perform()
                time.sleep(2)
                ele.find_element_by_class_name('renameBtn').click()

                filterDetail['filtername']=filterDetail['filtername']+"_new"
                filterDetailFromUI = saveNewFilter(setup, MRXConstants.SNFPOPUP, screenInstance,filterDetail,isEdit=True)
                if filterDetail['button'] == 'Save':
                    expected_detail = [filterDetail['filtername'], filterDetail['default']]
                    checkEqualAssert(expected_detail, filterDetailFromUI,message='Verify Entered detail after rename Save filter')

                filter_dict = getLoadFilterList(getHandle(setup, screenName, parent))
                checkEqualAssert(True,filter_dict.has_key(filterDetail['filtername']),message='Verify filter delete successfully')
                return
    except:
        logger.error('Not able click on delete button')
        return


def confirmDelete(setup,screenInstance,filterDetail):
    handle=getHandle(setup,MRXConstants.SNFPOPUP)
    if str(handle['allspans']['span'][0].text)=='Delete':
        logger.info('Get Popup for Confirm Delete')
        alertmsg=str(handle['alertMsg']['msg'][0].text)
        expectedMsg="Do you want to delete \""+str(filterDetail['filtername'])+"\" filter?"
        checkEqualAssert(expectedMsg,alertmsg,message='Verify Delete msg')
        if filterDetail['deleteFlag']=='True':
            screenInstance.clickButton("OK", getHandle(setup, MRXConstants.SNFPOPUP, Constants.ALLBUTTONS))
            return True
        else:
            screenInstance.clickButton("Cancel", getHandle(setup, MRXConstants.SNFPOPUP, Constants.ALLBUTTONS))
            return False
    else:
        logger.error('Confirm Delete Popup not found')
        resultlogger.error('Confirm Delete Popup not found')
        return False