from classes.Components.TimeRangeComponentClass import *
from MuralUtils.ContentHelper import *
from MuralUtils import UMHelper
from classes.Pages.MuralScreens.UserMangementScreen import *

try:

    setup = SetUp()
    #time.sleep(8)
    login(setup,MuralConstants.USERNAME,MuralConstants.PASSWORD)
    isError(setup)
    wfstart = WorkflowStartComponentClass()
    time.sleep(8)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    exploreScreenInstance.exploreList.switchApp(exploreHandle)
    userScreenInstance=UserManagementScreenClass(setup.d)
    result = exploreScreenInstance.exploreList.launchapp(getHandle(setup, "explore_Screen"), 2)
    checkEqualAssert(result, True, "", "", "Checking the launching of User Management")
    isError(setup)
    setup.d.switch_to.window(setup.d.window_handles[1])

    #UMHelper.deleteTableEntry(setup, MuralConstants.UserManagementScreen, 1, columnName="User Name")


    usersDetails=setup.cM.getNodeElements("userdetail","user")
    for k, usersDetail in usersDetails.iteritems():
        wfstart.clickImage('icon', getHandle(setup, MuralConstants.UserManagementScreen,'allimages'))

        try:
            userDetailFromUIPopup,listOfPrivileges=UMHelper.setUserDetail(setup,userScreenInstance,usersDetail,button=usersDetail['button'])
        except:
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved", r)
            resultlogger.debug("Got Exception because of invalid entry for New User:: Screenshot with name = %s is saved", r)
            getHandle(setup, MuralConstants.UserPopUpScreen,'icons')['icons']['closePopupIcon'][0].click()
            continue

        tableHandle = getHandle(setup, MuralConstants.UserManagementScreen,'table')
        tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
        if usersDetail['button']=='Create' and len(userDetailFromUIPopup)>0:
            checkEqualAssert(True,tableMap['rows'].has_key(usersDetail['username']),"","","Verify User added Successfully ")
            tableMap['rows'][usersDetail['username']].pop()
            PrivilegesFromTable=tableMap['rows'][usersDetail['username']].pop(4)
            checkEqualAssert(tableMap['rows'][usersDetail['username']],userDetailFromUIPopup,"","","Verify User Detail From table")

            listOfPrivilegesFromTable=PrivilegesFromTable.split(',')
            # neglecting User Management and System Monitoring from list of privileges in case of Admin
            if usersDetail['userrole']=='Admin':
                listOfPrivileges.remove('User Management')
                listOfPrivileges.remove('System Monitoring')


            for Privilege in listOfPrivileges:
                listOfPrivilegesFromTable.remove(Privilege)
            checkEqualAssert(0, len(listOfPrivilegesFromTable), '', '', 'Verify Privileges From Table')

        elif usersDetail['button']=='Create' and len(userDetailFromUIPopup)==0:
            checkEqualAssert(True, tableMap['rows'].has_key(usersDetail['username']), "", "","User aleady exist in table hence not allow to add again")

        elif usersDetail['button']=='Cancel':
            checkEqualAssert(False, tableMap['rows'].has_key(usersDetail['username']), "", "","After click on Cancel button user not added in table")

    #data=wfstart.getAllCheckBoxElement_UMMural(h,UserRole="1")
    #wfstart.clickCheckBoxWithName_UMMural(h,'Workflows.Reports',parent="allcheckboxes",child="checkbox",UserRole='1',force=True)
    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])
    setup.d.close()


    import suitemural_User_Management_Screen.UserCheckIn
    import suitemural_User_Management_Screen.EditUser
    import suitemural_User_Management_Screen.EditUserCheckIn
    import suitemural_User_Management_Screen.VerifyDeleteUser
    import suitemural_User_Management_Screen.VerifyEditUserForAdmin


except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()