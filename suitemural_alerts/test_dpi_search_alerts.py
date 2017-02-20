from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
setup=SetUp()
# sleep(6)
login(setup,"admin","admin123")

popInstance = GenerateReportsPopClass(setup.d)
# Launching DPI Alerts Page
popInstance.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
# doSearchAndValidateAlerts(setup)

doCalendarSearchOnAlerts(setup)


# Launching KPI Alerts Page
popInstance.dropdown.clickSpanWithTitle("KPI Alerts",getHandle(setup,MuralConstants.ALERTSCREEN,Constants.ALLSPANS))
doSearchAndValidateAlerts(setup)




setup.d.close()

# GUIDE_INFO