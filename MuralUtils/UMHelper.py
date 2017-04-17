from Utils.utility import *
from classes.Pages.GenerateReportsPopClass import GenerateReportsPopClass
from MuralConstants import *
from MuralUtils import Helper
from classes.Pages.MuralScreens.UserMangementScreen import *
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


def editUserDetail(setup,screenInstance,userDetail,button='Create'):

    detail = []

    h = getHandle(setup, MuralConstants.UserPopUpScreen)
    logger.info("Going to update UserRole for user =" + userDetail['username'])
    userRole_text = screenInstance.dropdown.doSelectionOnVisibleDropDown(h, str(userDetail['userrole']), index=0)
    checkEqualAssert(str(userDetail['userrole']), userRole_text, "", "", "Verify selected User Role")

    if str(userRole_text) == "Application":
        UserRole = '1'
    else:
        UserRole = '0'


    logger.info("Going to Update detail of user =" + userDetail['username'])
    userNameFromUI = str(h['allinputs']['editUserLabel'][0].text)
    detail.append(str(userNameFromUI))

    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 0)
    checkEqualAssert(str(firstNameFromUI), str(userDetail['firstname']), "", "", "Verify Entered First Name")
    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 1)
    checkEqualAssert(str(lastNameFromUI), str(userDetail['lastname']), "", "", "Verify Entered Last Name")
    detail.append(str(firstNameFromUI) + " " + str(lastNameFromUI))

    logger.info("Going to set Email =%s" + userDetail['email'])
    emailFromUI = screenInstance.cm.sendkeys_input(userDetail['email'], h, 0, child="email")
    checkEqualAssert(str(emailFromUI), str(userDetail['email']), "", "", "Verify Entered Email")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='email', index=0):
        raise
    detail.append(str(emailFromUI))
    detail.append(str(userRole_text))

    logger.info('Going to set enabled slider =%s for user =%s', userDetail['enabled'], userDetail['username'])
    colorOfEnabled = findPropertyColor(screenInstance, h, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=0)
    if (userDetail['enabled'] == "1" and str(colorOfEnabled) != MuralConstants.WHITECOLOR) or (userDetail['enabled'] == "0" and str(colorOfEnabled) == MuralConstants.WHITECOLOR):
        screenInstance.cm.click(h['allsliders']['slider'][0])
        if findPropertyColor(screenInstance, h, property=Constants.BACKGROUNDCOLOR, parent='allsliders', child='slider',index=0) == Constants.WHITECOLOR:
            status = Constants.ACTIVE_STATUS
        else:
            status = Constants.INACTIVE_STATUS
    elif userDetail['enabled'] == "1" and str(colorOfEnabled) == MuralConstants.WHITECOLOR:
        status = Constants.ACTIVE_STATUS
    elif userDetail['enabled'] != "1" and str(colorOfEnabled) != MuralConstants.WHITECOLOR:
        status = Constants.INACTIVE_STATUS
    detail.append(status)

    logger.debug('Going to click on update Password')
    h['allinputs']['updatePwd'][0].click()

    logger.info("Going to update Password =%s", userDetail['password'])
    passwordFromUI = screenInstance.cm.sendkeys_input(userDetail['password'], h, 0, child="password")
    checkEqualAssert(str(passwordFromUI), str(userDetail['password']), "", "", "Verify Entered Password")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='password', index=0):
        raise

    logger.info("Going to set Confirm Password =%s", userDetail['cpassword'])
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h, 1, child="password")
    checkEqualAssert(str(cpasswordFromUI), str(userDetail['cpassword']), "", "", "Verify Entered Password")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='password', index=1):
        raise

    password = screenInstance.cm.getValue_input(h, 0, child="password")
    cpassword = screenInstance.cm.getValue_input(h, 1, child="password")
    checkEqualAssert(str(password), str(cpassword), "", "", "Verify Password")

    logger.info("Going to set privileges =%s", userDetail['value'])
    privileges_list = str(userDetail['value']).split(',')

    if UserRole == '1':
        if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_WORKFLOWS) == 1:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_WORKFLOWS, UserRole=UserRole,force=True)
        if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI) == 1:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI, UserRole=UserRole,force=True)

        for value in privileges_list:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h, value, UserRole=UserRole)

    detailofcheckbox, checklist, unchecklist = screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))

    if button == "Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(button, getHandle(setup,MuralConstants.UserPopUpScreen,'allbuttons'))
        return [],[]

    if button == "Update":
        logger.info('Going to Click on %s Button', button)
        click_status = screenInstance.cm.clickButton(button, getHandle(setup,MuralConstants.UserPopUpScreen,'allbuttons'))
        checkEqualAssert(True, click_status, "", "", "Verify whether " + button + " button clicked or not")
        flag, msg = confirm(setup)
        if flag == True:
            h['icons']['closePopupIcon'][0].click()
            return [], []
        checkEqualAssert(0, len(getHandle(setup, MuralConstants.UserPopUpScreen, 'allbuttons')['allbuttons']['button']),"", "", "Verify Popscreen close after click on button =" + button)
    return detail, checklist




def setUserDetail(setup,screenInstance,userDetail,button='Create'):
    detail=[]
    flag_usename = False
    flag_email = False
    flag_password = False
    flag_cpassword = False

    logger.info("Going to select UserRole for user ="+userDetail['username'])
    userRole_text = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup, MuralConstants.UserPopUpScreen), str(userDetail['userrole']), index=0)
    checkEqualAssert(str(userDetail['userrole']), userRole_text, "", "", "Verify selected User Role")

    if str(userRole_text)=="Application":
        UserRole = '1'
    else:
        UserRole='0'

    h = getHandle(setup, MuralConstants.UserPopUpScreen)
    logger.info("Going to Enter detail of user ="+userDetail['username'])

    logger.info("Going to set UserName =%s" + userDetail['username'])
    userNameFromUI = screenInstance.cm.sendkeys_input(userDetail['username'],h,0)
    checkEqualAssert(str(userNameFromUI),str(userDetail['username']),"","","Verify Entered User Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR, index=0):
        raise
    flag_usename=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "UserName", screenInstance,setup)
    detail.append(str(userNameFromUI))


    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 1)
    checkEqualAssert(str(firstNameFromUI), str(userDetail['firstname']), "", "", "Verify Entered First Name")
    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 2)
    checkEqualAssert(str(lastNameFromUI), str(userDetail['lastname']), "", "", "Verify Entered Last Name")
    detail.append(str(firstNameFromUI)+" "+str(lastNameFromUI))

    logger.info("Going to set Email =%s" + userDetail['email'])
    emailFromUI= screenInstance.cm.sendkeys_input(userDetail['email'],h,0,child="email")
    checkEqualAssert(str(emailFromUI), str(userDetail['email']), "", "", "Verify Entered Email")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR,child='email', index=0):
        raise
    detail.append(str(emailFromUI))
    flag_email=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Email", screenInstance,setup)
    detail.append(str(userRole_text))


    logger.info('Going to set enabled slider =%s for user =%s',userDetail['enabled'],userDetail['username'])
    colorOfEnabled=findPropertyColor(screenInstance,h,property=Constants.BACKGROUNDCOLOR,parent='allsliders',child='slider',index=0)
    if (userDetail['enabled']=="1" and str(colorOfEnabled)!=MuralConstants.WHITECOLOR) or (userDetail['enabled']=="0" and str(colorOfEnabled)==MuralConstants.WHITECOLOR):
        screenInstance.cm.click(h['allsliders']['slider'][0])
        if findPropertyColor(screenInstance,h,property=Constants.BACKGROUNDCOLOR,parent='allsliders',child='slider',index=0)==Constants.WHITECOLOR:
            status=Constants.ACTIVE_STATUS
        else:
            status=Constants.INACTIVE_STATUS
    elif userDetail['enabled']=="1" and str(colorOfEnabled)==MuralConstants.WHITECOLOR:
        status=Constants.ACTIVE_STATUS
    elif userDetail['enabled']!="1" and str(colorOfEnabled)!=MuralConstants.WHITECOLOR:
        status = Constants.INACTIVE_STATUS
    detail.append(status)


    logger.info("Going to set Password =%s",userDetail['password'])
    passwordFromUI=screenInstance.cm.sendkeys_input(userDetail['password'],h,0,child="password")
    checkEqualAssert(str(passwordFromUI), str(userDetail['password']), "", "", "Verify Entered Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR,child='password', index=0):
        raise
    flag_password=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Password", screenInstance,setup)


    logger.info("Going to set Confirm Password =%s",userDetail['cpassword'])
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h,1,child="password")
    checkEqualAssert(str(cpasswordFromUI), str(userDetail['cpassword']), "", "", "Verify Entered Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR,child='password', index=1):
        raise
    flag_cpassword=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Confirm Password", screenInstance,setup)

    password=screenInstance.cm.getValue_input(h,0,child="password")
    cpassword=screenInstance.cm.getValue_input(h,1,child="password")
    checkEqualAssert(str(password), str(cpassword), "", "", "Verify Password")


    logger.info("Going to set privileges =%s",userDetail['value'])
    privileges_list=str(userDetail['value']).split(',')

    if UserRole=='1':
        if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h,Constants.UM_PARENT_WORKFLOWS)==1:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h,Constants.UM_PARENT_WORKFLOWS,UserRole=UserRole,force=True)
        if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI)== 1:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI, UserRole=UserRole, force=True)

        for value in privileges_list:
            screenInstance.cm.clickCheckBoxWithName_UMMural(h,value,UserRole=UserRole)

    detailofcheckbox,checklist,unchecklist=screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))
    button_status=dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword , "All Field",screenInstance,setup)

    if not button_status:
        logger.info("*************Create Button not enable**********")
        raise

    if button_status and button=="Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(button, getHandle(setup,MuralConstants.UserPopUpScreen,'allbuttons'))
        return [],[]

    if button_status and button=="Create":
        logger.info('Going to Click on %s Button',button)
        click_status=screenInstance.cm.clickButton(button,getHandle(setup,MuralConstants.UserPopUpScreen,"allbuttons"))
        checkEqualAssert(True,click_status,"","","Verify whether "+button+" button clicked or not")
        flag,msg=confirm(setup)
        if flag==True:
            h['icons']['closePopupIcon'][0].click()
            return [],[]
        checkEqualAssert(0,len(getHandle(setup,MuralConstants.UserPopUpScreen,'allbuttons')['allbuttons']['button']),"","","Verify Popscreen close after click on button ="+button)

    return detail,checklist



def dumpResultForButton(condition,request,screenInstance,setup,button_label="Create"):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup, MuralConstants.UserPopUpScreen,"allbuttons"))
    checkEqualAssert(condition,button_status,"","","Checking State of Create/Submit Button for Fields entered : "+str(request))
    return button_status


def sortTable(setup,insatnce,columnName="Name"):
    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, "table")
    insatnce.table.sortTable1(tableHandle, columnName)
    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, "table")

    data2 = insatnce.table.getTableData1(tableHandle)
    columnIndex = insatnce.table.getIndexForValueInArray(data2['header'], columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col, reverse=True), col, "", "", "Checking ColumnName Sort : " + columnName)
    logger.info("Sorted")
    cdata2 = insatnce.table.convertDataToDict(data2,key='User Name')
    return cdata2


def VerifyBasicTableFuncationality(setup,screenInstance,parent='table'):
    columns = setup.cM.getNodeElements("umsorttablecolumn", "column")
    column_names = []
    for k, column in columns.iteritems():
        column_names.append(column['locatorText'])

    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, parent)
    tableMap = screenInstance.table.getTableDataMap(tableHandle, driver=setup)

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




def deleteTableEntry(setup,screen,index,columnName,flag=True):

    screenInstance = UserManagementScreenClass(setup.d)
    tableHandle = getHandle(setup,screen,"table")
    tableData = screenInstance.table.getTableData1(tableHandle)
    # tableDataMap = screenInstance.table.convertDataToDict(tableData,columnName)
    rowToDelete = screenInstance.table.getColumnValueMap(tableData,index,columnName)
    logger.info("Going to delete table entry %s",str(rowToDelete))

    screenInstance.dropdown.customClick(tableHandle['table']['delete'][index])
    try:
        screenInstance.dropdown.customClick(getHandle(setup,screen,"table")['table']['delete'][index])
    except:
        pass
    return checkDeletedRow(setup, screen, screenInstance,columnName, rowToDelete, flag)



def checkDeletedRow(setup, screen, screenInstance,columnName, rowToDelete, flag):
    gHandle = getHandle(setup,screen,"umalert")
    button="Ok" if flag else "Cancel"

    popUpMessage = gHandle['umalert']['filters'][0].text.strip().strip('\n').strip()
    expectedMessage = "Do you want to delete "+rowToDelete.keys()[0]+" ?"

    actualHeader = gHandle['umalert']['header'][0].text.strip().strip('\n').strip()
    expectedHeader = "Delete"
    checkEqualAssert(expectedMessage,popUpMessage,"","","Verify Delete Dialog text")
    checkEqualAssert(expectedHeader,actualHeader,"","","Verify Delete Dialog Header")

    try:
        logger.debug("Clicking Button from Pop up %s",button)
        screenInstance.clickButton(button,gHandle,"umalert")
        try:
            screenInstance.clickButton(button,gHandle,"umalert")
            # gHandle['alert'][button][0].click()
        except:
            pass
        tableHandle = getHandle(setup,screen,"table")
        newTableData = screenInstance.table.getTableMap(tableHandle,columnName=columnName)

        checkEqualAssert(flag, rowToDelete.keys()[0] not in newTableData.keys(), "", "", "Check for Delete Table Entry" + str(rowToDelete))
        return True
    except Exception as e:
        logger.error("Exception found while Deleting Row %s : %s", rowToDelete, e)
        return e


def VerifyChangePasswordAndUserPrivileges(setup,screenInstance,handle,usersDetail,listOfPrivilegesFromTable,button='Change'):

    if len(handle['allinputs']['password'])>0:

        flag_current_password= False
        flag_new_password = False
        flag_new_cpassword=False

        logger.info("Going to Enter Current Password =%s",usersDetail['currentpassword'])
        currentpasswordfromUI = screenInstance.cm.sendkeys_input(usersDetail['currentpassword'], handle,0,child='password')
        checkEqualAssert(str(currentpasswordfromUI), str(usersDetail['currentpassword']), "", "", "Verify Current Password")
        #if not isColorValid(screenInstance, handle, property=Constants.BORDERCOLOR,child='password',index=0):
         #   raise
        flag_current_password = True
        dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword , "Current Password", screenInstance, setup,button_label="Change")

        logger.info("Going to Enter New Password =%s" + usersDetail['newpassword'])
        newpasswordFromUI = screenInstance.cm.sendkeys_input(usersDetail['newpassword'], handle,1, child="password")
        checkEqualAssert(str(newpasswordFromUI), str(usersDetail['newpassword']), "", "", "Verify Entered Password")
        # if len(getHandle(setup, MuralConstants.ChangePasswordScreen,'errormsg')['errormsg']['msg'])>0:
        #     logger.info('Password = %s is not valid',newpasswordFromUI)
        #     resultlogger.info('Password = %s is not valid',newpasswordFromUI)
        #     logger.debug()
        #if not isColorValid(screenInstance, handle, property=Constants.BORDERCOLOR,child='password', index=1):
        #    raise
        flag_new_password = True
        dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword, "New Password", screenInstance, setup,button_label="Change")

        logger.info("Going to set Confirm Password =%s" + usersDetail['newcpassword'])
        newcpasswordFromUI = screenInstance.cm.sendkeys_input(usersDetail['newcpassword'],handle, 2, child="password")
        checkEqualAssert(str(newcpasswordFromUI), str(usersDetail['newcpassword']), "", "", "Verify Entered Password")
        #if not isColorValid(screenInstance, handle, property=Constants.BORDERCOLOR,child='password', index=2):
        #    raise
        flag_newcpassword = True
        button_status = dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword,"All Field on Change Password Screen", screenInstance, setup,button_label='Change')

        if button_status and (button == "Change" or button == "Cancel"):
            click_status = screenInstance.cm.clickButton(button, handle)
            checkEqualAssert(True, click_status, "", "", "Verify whether " + button + " button clicked or not")
            h=getHandle(setup, MuralConstants.ChangePasswordScreen)
            if len(h)>0:
                if len(h['errormsg']['msg'])>0:
                    logger.error('Error found during Change Password =%s',str(h['errormsg']['msg'][0].text))
                    resultlogger.error('Error found during Change Password =%s',str(h['errormsg']['msg'][0].text))
                    logger.debug("Going to re-enter correct value")
                    screenInstance.cm.sendkeys_input(usersDetail['password'], handle, 0,child='password')
                    screenInstance.cm.clickButton(button, handle)
                    checkEqualAssert(0,len(getHandle(setup, MuralConstants.ChangePasswordScreen)['errormsg']['msg']),'Verify Change Password PopUp close after correct Password ')
            isError(setup)
            login(setup, usersDetail['username'], usersDetail['newpassword'])
            isError(setup)

    if usersDetail['userrole']=='Admin':
        listOfPrivilegesFromTable.append('User Management')
        listOfPrivilegesFromTable.append('System Monitoring')

    for Privileges in listOfPrivilegesFromTable:
        privileges=Privileges.replace(' ','')
        privileges =privileges.replace('/', '')
        function="check"+privileges
        getattr(CheckPrivileges(BasePageClass),function)(setup)


def verifySearch(setup,value,minimumcount,instance):

    logger.info("Going to find User =%s through search",value)
    h = getHandle(setup, MuralConstants.UserManagementScreen, 'allinputs')
    valuefromscreen = instance.cm.sendkeys_input(value, h, 0)
    checkEqualAssert(value, str(valuefromscreen), '', "", "Verify entered search text with search input ")


    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
    data2 = instance.table.getTableData1(tableHandle)

    if data2['rows']==Constants.NODATA:
        logger.debug('Entry for user = %s not found through search',value)
        resultlogger.debug('Entry for user = %s not found through search',value)
        return
    else:
        checkEqualAssert(True, len(data2['rows']) >= minimumcount, '', '',"Verify total search result for =" + value)
        for i in range(len(data2['rows'])):
            checkEqualAssert(True, value in str(data2['rows'][i][0]).strip(), '', '', 'Verify serach result for ='+value)

    instance.cm.sendkeys_input(Keys.ENTER, h, 0, clear=False)
    time.sleep(3)

def verifyAdminNotDeletable(setup,instance):

    h = getHandle(setup, MuralConstants.UserManagementScreen, 'allinputs')
    valuefromsearchbox = instance.cm.sendkeys_input('admin', h, 0)
    checkEqualAssert('admin', str(valuefromsearchbox), '', "", "Verify entered search text with search input ")
    isError(setup)

    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
    index = instance.table.getRowIndexFromTable(0, tableHandle, 'admin')
    if index == -1:
        logger.debug('************Entry for admin not found in table**************')
        resultlogger.debug('***********Entry for admin not found in table*************')
    try:
        tableHandle['table']['delete'][index].click()
    except Exception as e:
        checkEqualAssert(False, e, '', '',"Verify that admin from table is not deletable  ==> Delete functionlaity should be handled")

    data2 = instance.table.getTableData1(tableHandle)
    for i in range(len(data2['rows'])):
        checkEqualAssert(True, 'admin' in str(data2['rows'][i][0]).strip(), '', '', 'Verify serach result for admin')

    instance.cm.sendkeys_input(Keys.ENTER, h, 0, clear=False)
    isError(setup)


def clickOnLinkByValue(setup,screenName,value,parent='appHeader',child='alllinks'):
    try:
        exploreHandle=getHandle(setup, screenName)
        for i in range(len(exploreHandle[parent][child])):
            if str(exploreHandle[parent][child][i].text) == str(value):
                exploreHandle[parent][child][i].click()
                return True
        return False
    except:
        logger.debug("Not able to click on %s",value)
        resultlogger.debug("Not able to click on %s", value)
        return False


def getUserDetailFromUI(setup,screenInstance):
    detail = []
    h = getHandle(setup, MuralConstants.UserPopUpScreen)
    userRole_text = screenInstance.dropdown.getSelectionOnVisibleDropDown(h,index=0)

    userNameFromUI = str(h['allinputs']['editUserLabel'][0].text)
    detail.append(str(userNameFromUI))

    firstNameFromUI = screenInstance.cm.getValue_input(h, 0)
    lastNameFromUI = screenInstance.cm.getValue_input( h, 1)
    detail.append(str(firstNameFromUI) + " " + str(lastNameFromUI))

    emailFromUI = screenInstance.cm.getValue_input(h, 0, child="email")
    detail.append(str(emailFromUI))

    detail.append(str(userRole_text))

    colorOfEnabled = findPropertyColor(screenInstance, h, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=0)
    if (str(colorOfEnabled) != MuralConstants.WHITECOLOR) :
        status = Constants.INACTIVE_STATUS
    else:
        status = Constants.ACTIVE_STATUS
    detail.append(status)

    detailofcheckbox, checklist, unchecklist = screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))

    return detail, checklist

