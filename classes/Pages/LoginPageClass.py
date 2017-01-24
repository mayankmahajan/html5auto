from BasePageClass import BasePageClass
from classes.Components.BaseComponentClass import BaseComponentClass
import classes.DriverHelpers.DriverHelper


class LoginPageClass(BasePageClass):
    def __init__(self, driver):
        # BasePageClass.__init__(driver)
        self.driver = driver
        self._username = BaseComponentClass()
        self._password = BaseComponentClass()
        self._signin = BaseComponentClass()

    def getUserNameText(self, elHandle):
        return self._username.text(elHandle)

    def setUserName(self, elHandle, value):
        self._username.send_keys(elHandle, value)

    def getPasswordText(self, elHandle):
        return self._password.text(elHandle)

    def setPassword(self, elHandle, value):
        self._password.send_keys(elHandle, value)

    def signIn(self, elHandle):
        self._signin.click(elHandle)
