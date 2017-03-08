from MuralUtils import NetworkHelper
from Utils.SetUp import *
from classes.Pages.MuralScreens.NetworkScreenClass import *


setup =SetUp()
nScreenIntance = NetworkScreenClass(setup.d)
NetworkHelper.doActionsOnNetwork(nScreenIntance,setup)

