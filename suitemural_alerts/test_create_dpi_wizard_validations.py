from Utils.SetUp import *
from MuralUtils import AlertsHelper
from Utils.utility import *
from classes.Objects.CreateAlert import *

setup=SetUp()
sleep(6)
login(setup,"admin","admin123")
x =CreateAlert()

AlertsHelper.validateDPIAlertWizard(setup,x.dict)

# GUIDE_INFO