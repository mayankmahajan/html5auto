import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *

# Getting Setup Details
setup = SetUp()

# Launching Application
login(setup, "admin", "Admin@123")

# Launch Site Screen
launchPage(setup,"site_Screen")

# Result Logging
softequalAssert("mayank",setup.d.current_url)


# Closing the Testcase
setup.d.close()