import unittest
from Utils.logger import *
from selenium import webdriver

from Utils.utility import *
from classes.DriverHelpers.DriverHelper import DriverHelper
from Utils.Constants import *
from Utils.SetUp import *
from classes.Pages.FPVPageClass import FPVPageClass

setup = SetUp()

login(setup, "admin", "Admin@123")
fpvInstance = FPVPageClass(setup.d)
fpvHandler = getHandle(setup,"fpv_screen","fpv")

data = fpvInstance.fpv.getData(fpvHandler)

# Closing the Testcase
setup.d.close()