from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
from classes.Objects.CreateAlert import *

x =CreateAlert()
setup=SetUp()

# units1=setup.cM.getNodeElements("unitsystem","unit")
# measures1= setup.cM.getNodeElements("measures","measure")
# measuretypes = setup.cM.mergeTwoNodes(measures1,units1,"unitSystem")

# request = {}
# request['ruleName'] = "automationRuleName"
# request['measureName'] = "Hits"
# request['type'] = "Rate Of Change"
# request['gran'] = "Daily"
# sleep(6)

login(setup,"admin","admin123")
print createDPIAlert(setup, x.dict)

# GUIDE_INFO

setup.d.close()