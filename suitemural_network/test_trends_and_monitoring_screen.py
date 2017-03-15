from MuralUtils import NetworkHelper
from Utils.SetUp import *
from classes.Pages.MuralScreens.NetworkScreenClass import *
from MuralUtils.MuralConstants import *
from classes.Components.WorkflowStartComponent import *
from MuralUtils import Helper
from classes.Pages.GlobalFiltersPopClass import *

try:
    setup =SetUp()
    # Launching Network Screen
    wfstart = WorkflowStartComponentClass()
    # sleep(8)
    wfstart.launchScreen("Network",getHandle(setup,MuralConstants.WFSTARTSCREEN))

    globalFilterInstance = GlobalFiltersPopClass(setup.d)
    networkScreenInstance = NetworkScreenClass(setup.d)

    # launch Global Filters PopUp
    ### code will come here to launch it

    # filter text shown at popup
    f1 = Helper.setGlobalFilters(globalFilterInstance,setup)
    popUpTooltipData = Helper.getGlobalFiltersToolTipData(MuralConstants.GFPOPUP,globalFilterInstance,setup)

    # apply global filters
    globalFilterInstance.clickButton("Apply",getHandle(setup,MuralConstants.GFPOPUP,MuralConstants.ALLBUTTONS))

    # get global filter from Screen
    f = Helper.getGlobalFiltersFromScreen(MuralConstants.NWSCREEN,globalFilterInstance,setup)
    popUpTooltipData1 = Helper.getGlobalFiltersToolTipData(MuralConstants.NWSCREEN,globalFilterInstance,setup)

    # Test All functionality on the screen
    NetworkHelper.testScreenFunc(setup,networkScreenInstance)

    setup.d.close()
except Exception as e:
    print str(e)
    # sys._current_frames()
    setup.d.close()
    raise e



