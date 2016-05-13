from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    SIGNIN = (By.CSS_SELECTOR, '[ng-click = "vm.login()"]')
    USERNAME = (By.ID, 'username')
    PASSWORD = (By.ID, 'password')


class ExplorePageLocators(object):
    SITES = (By.XPATH, '//*[contains(@id, "exploreLabel0")]')

class SitePageLocators(object):
    BTV = (By.XPATH, '//*[contains(@id, "_barTabularView")]')
    SELECTIONLABEL = (By.XPATH, '//*[contains(@class, "selectionLabel")]')
    # RIGHTSELECTIONLABEL = (By.XPATH, '//*[@class="selectionLabel" and @style="max-width: 500px;"]')
    RIGHTSELECTIONLABEL = (By.CSS_SELECTOR, '[style=" max-width: 500px;"]')
    # SELECTIONLABEL = (By.XPATH, '//*[@class="selectionLabel"]')

