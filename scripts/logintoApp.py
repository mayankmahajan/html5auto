from selenium import webdriver
from pages.commonPage import LoginElements,ExploreElements,SiteElements
from scripts.Constants import Constants

class LoginApp():


    def login(self,driver):

        self.loginElements.get_userName_element(driver).send_keys(Constants.USERNAME)
        self.loginElements.get_password_element(driver).send_keys(Constants.PASSWORD)
        self.loginElements.get_signIn_element(driver).click()

    def __init__(self,driver):
        # self.driver = webdriver.Firefox()
        driver.get(Constants.URL)
        self.loginElements = LoginElements(driver)

