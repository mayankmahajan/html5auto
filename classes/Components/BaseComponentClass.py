# from classes.DriverHelpers.DriverHelper import DriverHelper
# from selenium import webdriver
# webdriver.Firefox().find_element_by_xpath().send_keys()

class BaseComponentClass:
    def m_click(self,elHandle):
        return elHandle.click()
    def m_send_keys(self,elHandle,value):
        return elHandle.send_keys(value)
    def text(self,elHandle):
        return elHandle.text


