from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.ForensicsPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")


exploreScreenInstance.exploreList.switchApp(exploreHandle)
result = exploreScreenInstance.exploreList.launchapp(getHandle(setup,"explore_Screen"),2)

time.sleep(4)
setup.d.switch_to.window(setup.d.window_handles[1])

forensicsScreenInstance = ForensicsPageClass(setup.d)
forensicsScreenHandle = getHandle(setup,"forensics_Screen")

view = forensicsScreenInstance.dropdown.click(forensicsScreenHandle['netflowtable']['view'][1])
checkEqualAssert(view,True,"","","View button validation")
forensicsScreenHandle = getHandle(setup,"forensics_Screen","allbuttons")
downloadnetflow = forensicsScreenInstance.reportspopup.clickButton("Download",forensicsScreenHandle)
checkEqualAssert(downloadnetflow,True,"","","Download Netflow Button Validation")
forensicsScreenHandle = getHandle(setup,"forensics_Screen","configurebutton")
forensicsScreenInstance.reportspopup.customClick(forensicsScreenHandle['configurebutton']['configure'])
popupInstance = GenerateReportsPopClass(setup.d)
####### Get the Handles of the routers Popup#################
popupHandler = getHandle(setup,"routers_popup","routertable")
popupInstance.table.setSpecialSelection(setup.d,[2,4],Keys.COMMAND,popupHandler,"routertable")

popupHandler = getHandle(setup,"routers_popup","footerbuttons")
fields = popupInstance.reportspopup.clickButton("OK",popupHandler,"footerbuttons")
checkEqualAssert(fields,True,"","","New Fields Validation")
forensicsScreenHandle = getHandle(setup,"forensics_Screen","allbuttons")
forensicsScreenInstance.reportspopup.clickButton("Delete",forensicsScreenHandle)
forensicsScreenHandle = getHandle(setup,"forensics_Screen","allbuttons")
deletenetflow =forensicsScreenInstance.reportspopup.clickButton("Ok",forensicsScreenHandle)
checkEqualAssert(deletenetflow,True,"","","Delete Netflow Button Validation")

setup.d.close()
setup.d.switch_to.window(setup.d.window_handles[0])
setup.d.close()
