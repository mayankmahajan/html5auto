from Utils.SetUp import *
from MuralUtils import AlertsHelper
from Utils.utility import *

setup=SetUp()
login(setup,"admin","admin123")


AlertsHelper.validateKPIAlertWizard(setup)

# GUIDE_INFO
setup.d.close()