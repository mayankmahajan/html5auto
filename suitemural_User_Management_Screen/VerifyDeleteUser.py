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

    h = getHandle(setup, MuralConstants.UserManagementScreen, 'allinputs')
    userScreenInstance.cm.sendkeys_input('Guavus_123', h, 0)
    #userScreenInstance.cm.sendkeys_input('praveen', h, 0)
    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
    data2 = userScreenInstance.table.getTableData1(tableHandle)
    index=userScreenInstance.table.getRowIndexFromTable(0,tableHandle,'Guavus_123')
    #index = userScreenInstance.table.getRowIndexFromTable(0, tableHandle, 'praveen')
    logger.debug("Going to Click Delete Button for user =%s",'Guavus_123')
    resultlogger.debug("Going to Click Delete Button for user =%s",'Guavus_123')

    try:
        setup.d.execute_script("arguments[0].click()", tableHandle['table']['delete'][index])

    except Exception as e:
        logger.debug("Not able to click on Delete for user = %s ", 'Guavus_123')
        resultlogger.debug("Not able to click on Delete for user = %s ", 'Guavus_123')

    flag,msg=confirm(setup)
    if not flag:
        flag, msg = confirm(setup)

    userScreenInstance.cm.sendkeys_input(Keys.ENTER, h, 0, clear=False)

    tableHandle = getHandle(setup, MuralConstants.UserManagementScreen, 'table')
    tableMap = userScreenInstance.table.getTableDataMap(tableHandle, driver=setup)
    checkEqualAssert(False, tableMap['rows'].has_key('Guavus_123'), "", "","Verify User Deleted Successfully ")
    #checkEqualAssert(False, tableMap['rows'].has_key('praveen'), "", "","Verify User Deleted Successfully ")

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