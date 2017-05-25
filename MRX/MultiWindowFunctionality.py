from Utils.SetUp import *
from classes.Components.TimeRangeComponentClass import *
from classes.Pages.MRXScreens.SegmentScreenClass import *
from MRXUtils.MRXConstants import *

NumberofWindow=2

try:
    handle_list = []
    setup = SetUp()
    handle_list.append(setup)
    login(setup, Constants.USERNAME, Constants.PASSWORD)
    segmentScreenInstance = SegmentScreenClass(setup.d)
    tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
    data2 = segmentScreenInstance.table.getTableData1(tableHandle)


    for i in range(1,NumberofWindow):
        setup = SetUp()
        handle_list.append(setup)
        login(setup, Constants.USERNAME, Constants.PASSWORD)
        tableHandle = getHandle(setup, MRXConstants.SEGMENTSCREEN, 'table')
        data3 = segmentScreenInstance.table.getTableData1(tableHandle)
        checkEqualAssert(data2,data3,message='Verify the behaviour when same user opens the UI in two tabs and perform some action on it',testcase_id='MKR-1741')


    for i in range(len(handle_list)):
        handle=handle_list.pop()
        handle.d.close()



except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    raise e
    setup.d.close()