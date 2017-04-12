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

    def setUserName(self, elHandle, value,parent="username",child="username",occurence=0):
        self._username.sendkeys_input(value,elHandle,occurence,parent,child)
        # self._username.send_keys(elHandle, value)

    def getPasswordText(self, elHandle):
        return self._password.text(elHandle)

    def setPassword(self, elHandle, value,parent="password",child="password",occurence=0):
        self._password.sendkeys_input(value,elHandle,occurence,parent,child)

    def signIn(self, elHandle,parent="signin",child="signin",occurence=0):
        self._signin.click(elHandle[parent][child][occurence])
