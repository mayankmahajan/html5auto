from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    SIGNIN = (By.CSS_SELECTOR, '[ng-click = "vm.login()"]')
    USERNAME = (By.ID, 'username')
    PASSWORD = (By.ID, 'password')


class ExplorePageLocators(object):
    SITES = (By.XPATH, '//*[contains(@id, "exploreLabel0")]')
    EXPLORELIST = (By.CSS_SELECTOR,'[ng-mouseover="vm.showTooltip(startPoint,$index)"]')

class BTVLocators(object):
    BTV = (By.XPATH, '//*[contains(@id, "_barTabularView")]')
    BTVCOLUMN0 = (By.XPATH, '//*[contains(@class, "column0")]')
    BTVCOLUMN1 = (By.XPATH, '//*[contains(@class, "column1")]')
    BTVCOLUMN2 = (By.XPATH, '//*[contains(@class, "column2")]')
    SELECTIONS = (By.CSS_SELECTOR, '[background-color: rgb(70, 97, 111);]')


class ContextMenuLocators(object):
    # CONTEXTMENU = (By.ID, 'dl-menucontextMenuDisplay')
    DRILLTO = (By.ID,'frameworkDrill')
    SITETREND = (By.ID,'SITE_TREND_SCR')
    EXPORTTO = (By.ID,'exportDrill')

class ExportToLocators(object):
    EXPORTTOCSV = (By.ID,'EXPORT_TO_CSV')
    EXPORTTOSNAPSHOT = (By.ID,'EXPORT_TO_SNAPSHOT')

class DrillToLocators(object):
    # CONTEXTMENU = (By.ID, 'dl-menucontextMenuDisplay')
    #
    # DRILLTO = (By.ID,'frameworkDrill')
    # SITETREND = (By.ID,'SITE_TREND_SCR')
    # EXPORTTO = (By.ID,'exportDrill')
    #
    # EXPORTTOCSV = (By.ID,'EXPORT_TO_CSV')
    # EXPORTTOSNAPSHOT = (By.ID,'EXPORT_TO_SNAPSHOT')

    DRILLTONF = (By.ID,'NWT_FUNC_SCR')
    DRILLTOSITE = (By.ID,'SITE_SCR')
    DRILLTONE = (By.ID,'NETWORK_ELEMENT_SCR')
    DRILLTOSITEINTERACTION = (By.ID,'SITE_INTERACTION_SCR')
    DRILLTOVRF = (By.ID,'VRF_SCR')



class CommonElementLocators(object):
    CONTEXTMENU = (By.ID, 'dl-menucontextMenuDisplay')
    SELECTIONLABEL = (By.XPATH, '//*[contains(@class, "selectionLabel")]')
    RIGHTSELECTIONLABEL = (By.CSS_SELECTOR, '[style=" max-width: 500px;"]')

class SitePageLocators(object):
    # CONTEXTMENU = (By.ID, 'dl-menucontextMenuDisplay')
    SELECTIONLABEL = (By.XPATH, '//*[contains(@class, "selectionLabel")]')
    # RIGHTSELECTIONLABEL = (By.XPATH, '//*[@class="selectionLabel" and @style="max-width: 500px;"]')
    RIGHTSELECTIONLABEL = (By.CSS_SELECTOR, '[style=" max-width: 500px;"]')
    # SELECTIONLABEL = (By.XPATH, '//*[@class="selectionLabel"]')

