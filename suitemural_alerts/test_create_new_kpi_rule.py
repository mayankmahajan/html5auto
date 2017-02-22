from Utils.SetUp import *
from MuralUtils.AlertsHelper import *
from classes.Objects.CreateAlert import *
setup=SetUp()
sleep(6)
login(setup,"admin","admin123")
createKPIAlert(setup)

# GUIDE_INFO
setup.d.close()