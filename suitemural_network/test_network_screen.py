from MuralUtils import NetworkHelper
from Utils.SetUp import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from MuralUtils.MuralConstants import *
from classes.Components.WorkflowStartComponent import *
try:
    setup =SetUp()

    # Launching Network Screen
    wfstart = WorkflowStartComponentClass()
    sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))


    # Test All functionality on the screen
    NetworkHelper.setGlobalFilters(setup)
    NetworkHelper.testScreenFunc(setup)



    setup.d.close()
except Exception as e:
    print str(e)
    # sys._current_frames()
    setup.d.close()



