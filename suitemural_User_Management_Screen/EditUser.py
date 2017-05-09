from classes.Components.TimeRangeComponentClass import *
from MuralUtils.ContentHelper import *
from MuralUtils import UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *

try:

    setup = SetUp()
    login(setup, MuralConstants.USERNAME, MuralConstants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    time.sleep(8)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.switchApp(exploreHandle)
    userScreenInstance = UserManagementScreenClass(setup.d)
    result = exploreScreenInstance.exploreList.launchapp(getHandle(setup, "explore_Screen"), 2)
    checkEqualAssert(result, True, "", "", "Checking the launching of User Management")
    isError(setup)
    setup.d.switch_to.window(setup.d.window_handles[1])

    usersDetails = setup.cM.getNodeElements("userdetail", "edituser")

    for k, usersDetail in usersDetails.iteritems():
        h = getHandle(setup, MuralConstants.UserManagementScreen, 'allinputs')
        userScreenInstance.cm.sendkeys_input(usersDetail['username'], h, 0)

        tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
        data2 = userScreenInstance.table.getTableData1(tableHandle)


        index=userScreenInstance.table.getRowIndexFromTable(0,tableHandle,usersDetail['username'])
        userDetailFromTable=[]
        for value in data2['rows'][index]:
            userDetailFromTable.append(value)

        logger.debug("Going to Click Edit Button for user =%s",usersDetail['username'])
        resultlogger.debug("Going to Click Edit Button for user =%s",usersDetail['username'])

        try:
            tableHandle['table']['edit'][index].click()
        except Exception as e:
            logger.debug("Not able to click on edit for user = %s ", usersDetail['username'])
            resultlogger.debug("Not able to click on edit for user = %s ", usersDetail['username'])
            continue

        userDetailFromUIPopup,listOfPrivileges=UMHelper.getUserDetailFromUI(setup,userScreenInstance)
        userDetailFromTable.pop()
        PrivilegesFromTable = userDetailFromTable.pop(4)
        checkEqualAssert(userDetailFromTable, userDetailFromUIPopup, "", "","Verify User Detail From table")

        listOfPrivilegesFromTable = PrivilegesFromTable.split(',')
        # neglecting User Management and System Monitoring from list of privileges in case of Admin
        if userDetailFromUIPopup[3] == 'Admin':
            listOfPrivileges.remove('User Management')
            listOfPrivileges.remove('System Monitoring')

        for Privilege in listOfPrivileges:
            listOfPrivilegesFromTable.remove(Privilege)
        checkEqualAssert(0, len(listOfPrivilegesFromTable), '', '', 'Verify Privileges From Table')

        updatedUserDetailFromUIPopup, updatedListOfPrivileges = UMHelper.editUserDetail(setup, userScreenInstance, usersDetail,button=usersDetail['button'])

        tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
        data2 = userScreenInstance.table.getTableData1(tableHandle)

        index = userScreenInstance.table.getRowIndexFromTable(0, tableHandle, usersDetail['username'])
        updatedUserDetailFromTable = []
        for value in data2['rows'][index]:
            updatedUserDetailFromTable.append(value)

        updatedUserDetailFromTable.pop()
        updatedPrivilegesFromTable = updatedUserDetailFromTable.pop(4)

        updatedListOfPrivilegesFromTable = updatedPrivilegesFromTable.split(',')

        if len(updatedUserDetailFromUIPopup)==0:
            checkEqualAssert(updatedUserDetailFromTable, userDetailFromTable, "", "","Verify that if we click on Cancel button than User's Detail remains same")

        else:
            if updatedUserDetailFromUIPopup[3] == 'Admin':
                updatedListOfPrivileges.remove('User Management')
                updatedListOfPrivileges.remove('System Monitoring')

            for Privilege in updatedListOfPrivileges:
                updatedListOfPrivilegesFromTable.remove(Privilege)

            checkEqualAssert(updatedUserDetailFromTable, updatedUserDetailFromUIPopup, "", "","Verify Updated User's Detail From table")
            checkEqualAssert(0, len(updatedListOfPrivilegesFromTable), '', '', 'Verify updated Privileges From Table')

        userScreenInstance.cm.sendkeys_input(Keys.ENTER, h, 0, clear=False)

    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()