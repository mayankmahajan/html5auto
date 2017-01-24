from Utils.SetUp import *
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Pages.ForensicsPageClass import *

setup = SetUp()

login(setup, "admin", "Admin@123")

setup.d.switch_to.window(setup.d.window_handles[1])

forensicsScreenInstance = ForensicsPageClass(setup.d)

forensicsScreenHandle = getHandle(setup,"forensics_Screen","configurebutton")
forensicsScreenInstance.reportspopup.customClick(forensicsScreenHandle['configurebutton']['configure'])
popupInstance = GenerateReportsPopClass(setup.d)
###### Get the Handles of the routers Popup#################
popupHandler = getHandle(setup,"routers_popup","routertable")
popupInstance.table.setSpecialSelection(setup.d,[2,4],Keys.COMMAND,popupHandler,"routertable")
data = popupInstance.table.getSelection(popupHandler,"routertable")
print data
popupHandler = getHandle(setup,"routers_popup","footerbuttons")
fields = popupInstance.reportspopup.clickButton("OK",popupHandler,"footerbuttons")
popuphandler = getHandle(setup,"routers_popup")
forensicsScreenHandle = getHandle(setup,"forensics_Screen")
# data1 = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"routertable")
data2 = forensicsScreenInstance.table.getTableData1(forensicsScreenHandle,"netflowtable")
print data2


setup.d.close()