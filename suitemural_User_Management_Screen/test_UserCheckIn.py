from classes.Components.TimeRangeComponentClass import *
from MuralUtils.ContentHelper import *
from MuralUtils import UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *

try:

    setup = SetUp()
    #time.sleep(8)
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

    # verify basic table functionality
    #logger.debug("Verify Basic Table functionality")
    #UMHelper.VerifyBasicTableFuncationality(setup,userScreenInstance)


    # UMHelper.verifyAdminNotDeletable(setup,userScreenInstance)
    #
    # usersDetails = setup.cM.getNodeElements("userdetail", "user")
    # totalUserAddedFromXML = []
    # listOfUserForSearch = []
    #
    # for k, usersDetail in usersDetails.iteritems():
    #     if usersDetail['button']=='Create' and ( usersDetail['id']=='0' or usersDetail['id']=='1' or usersDetail['id']=='2'):
    #         listOfUserForSearch.append(usersDetail['username'])
    #
    #     if usersDetail['button']=='Create':
    #         totalUserAddedFromXML.append(usersDetail['username'])
    #
    # for value in listOfUserForSearch:
    #     mini_count=0
    #     for user in totalUserAddedFromXML:
    #         if value in user:
    #            mini_count=mini_count+1
    #
    #     UMHelper.verifySearch(setup,value,mini_count,userScreenInstance)


    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
    tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    previousUserName='admin'
    usersDetails = setup.cM.getNodeElements("userdetail", "user")
    for k, usersDetail in usersDetails.iteritems():
        if tableMap['rows'].has_key(usersDetail['username']):
            checkEqualAssert(True, tableMap['rows'].has_key(usersDetail['username']), '', '',"Verify  Entry of User =" + usersDetail['username'] + " in table")
            logger.info("Going to login with User detail from table")
            tableMap['rows'][usersDetail['username']].pop()
            PrivilegesFromTable = tableMap['rows'][usersDetail['username']].pop(4)
            listOfPrivilegesFromTable = PrivilegesFromTable.split(',')

            handle=getHandle(setup,"user_popup")

            if len(handle['popupcontainer']['userIcon'])>0:
                handle['popupcontainer']['userIcon'][0].click()
                handle1 = getHandle(setup, "user_popup")
                handle1['popupcontainer']['popup'][0].click()
                time.sleep(5)

            exploreHandle = getHandle(setup, MuralConstants.ExploreScreen)
            if len(exploreHandle['appHeader']['alllinks'])>0:
                UMHelper.clickOnLinkByValue(setup,MuralConstants.ExploreScreen,previousUserName)
                UMHelper.clickOnLinkByValue(setup, MuralConstants.ExploreScreen, MuralConstants.Logout)
                time.sleep(5)

            login(setup, usersDetail['username'], usersDetail['password'])
            flag,msg=isError(setup)

            if flag==True:
                login(setup, usersDetail['username'], usersDetail['newpassword'])
                flagForCheckInactive,msg1=isError(setup)
                if flagForCheckInactive==True:
                    logger.debug("User is Inactive So not able to login")
                    continue
            change_password_screen_handle = getHandle(setup, MuralConstants.ChangePasswordScreen)
            UMHelper.VerifyChangePasswordAndUserPrivileges(setup,userScreenInstance,change_password_screen_handle,usersDetail,listOfPrivilegesFromTable,button="Change")
            previousUserName=usersDetail['username']
        else:
            if usersDetail['button']=='Create':
                checkEqualAssert(True,tableMap['rows'].has_key(usersDetail['username']),'','',"Verify  Entry of User ="+usersDetail['username']+" in table")

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