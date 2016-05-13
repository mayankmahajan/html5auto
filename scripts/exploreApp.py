from selenium import webdriver
from pages.commonPage import LoginElements,ExploreElements,SiteElements
from scripts.Constants import Constants

class ExploreApp():

    def gotoPage(self,driver,page):
        self.exploreElements.get_page_element(page).click()

    def __init__(self,driver):
        self.exploreElements = ExploreElements(driver)

