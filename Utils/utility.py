from Utils.logger import *
from classes.DriverHelpers.locators import *
from classes.Pages import ExplorePageClass
from classes.Pages.LoginPageClass import *
from classes.Pages.ExplorePageClass import *
from classes.Pages.SitePageClass import *
from classes.DriverHelpers.DriverHelper import *



def setupTestcase(self):
    self.driver = webdriver.Firefox()
    self.driverHelper = DriverHelper(self.driver)
    return True

def login(driver,driverHelper,username,password):
    try:
        loginPage = LoginPageClass(driver)
        usernameHandler = driverHelper.waitForVisibleElement(LoginPageLocators.USERNAME)
        loginPage.setUserName(usernameHandler,username)
        passwordHandler = driverHelper.waitForVisibleElement(LoginPageLocators.PASSWORD)
        loginPage.setPassword(passwordHandler,password)
        signinHandler = driverHelper.waitForVisibleElement(LoginPageLocators.SIGNIN)
        loginPage.signIn(signinHandler)

        logger.info('Login Successful')
        logger.debug('Username : %s',username)
        logger.debug('Password : %s',password)
        return True
    except ValueError:
        return ValueError

def launchPage(driver,driverHelper,pageName):
    try:
        explorePage = ExplorePageClass(driver)
        exploreListHandler = driverHelper.waitForVisibleElements(ExplorePageLocators.EXPLORELIST)
        for elHandler in exploreListHandler:
            if elHandler.text.upper() in pageName:
                explorePage.launchPage(elHandler)
                break
        logger.debug('Page Launched : %s',pageName)
        return True
    except ValueError:
        return ValueError

def getBTVData(driver,driverHelper):
    try:
        sitePage = SitePageClass(driver)
        btvHandler = driverHelper.waitForVisibleElement(BTVLocators.BTV)
        col1Handler = driverHelper.waitForVisibleElements(BTVLocators.BTVCOLUMN1)
        col2Handler = driverHelper.waitForVisibleElements(BTVLocators.BTVCOLUMN2)
        data = sitePage.getBTVData(btvHandler,col1Handler,col2Handler)
        for key,value in data.iteritems():
            logger.debug('Col1 : %s  and Col2 : %s',key,value )
        return data
    except ValueError:
        return ValueError