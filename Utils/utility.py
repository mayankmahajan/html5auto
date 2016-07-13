from Utils.logger import *
from classes.DriverHelpers.locators import *
from classes.Pages import ExplorePageClass
from classes.Pages.LoginPageClass import *
from classes.Pages.ExplorePageClass import *
from classes.Pages.SitePageClass import *
from classes.DriverHelpers.DriverHelper import *
from Utils.ConfigManager import ConfigManager
from copy import deepcopy



def setupTestcase(self):
    self.driver = webdriver.Firefox()
    self.driverHelper = DriverHelper(self.driver)
    return True

def login(driver,driverHelper,username,password):
    try:
        configmanager = ConfigManager()
        configs = configmanager.componentSelectors
        # configs = configmanager.getComponentConfigs()
        loginConfigs = deepcopy(configs)

        usernameHandler = driverHelper.waitForVisibleElement((loginConfigs['username']['selector'],loginConfigs['username']['locator']))
        passwordHandler = driverHelper.waitForVisibleElement((loginConfigs['password']['selector'],loginConfigs['password']['locator']))
        signinHandler = driverHelper.waitForVisibleElement((loginConfigs['signin']['selector'],loginConfigs['signin']['locator']))

        loginPage = LoginPageClass(driver)
        # usernameHandler = driverHelper.waitForVisibleElement(LoginPageLocators.USERNAME)
        loginPage.setUserName(usernameHandler,username)
        # passwordHandler = driverHelper.waitForVisibleElement(LoginPageLocators.PASSWORD)
        loginPage.setPassword(passwordHandler,password)
        # signinHandler = driverHelper.waitForVisibleElement(LoginPageLocators.SIGNIN)
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
        # exploreListHandler = driverHelper.waitForVisibleElements(ExplorePageLocators.EXPLORELIST)
        # elHandler = explorePage.exploreList.getHandlerToPage(exploreListHandler,pageName)

        configmanager = ConfigManager()
        # screenConfigs = deepcopy(configmanager.getScreenConfigs())
        screenConfigs = deepcopy(configmanager.componentSelectors)
        componentConfigsPerScreen = deepcopy(configmanager.getComponentConfigsPerScreen('exploreScreen'))

        locator = (screenConfigs['sites']['selector'],screenConfigs['sites']['locator'])
        elHandler = driverHelper.waitForVisibleElement(locator)
        # elHandler = explorePage.exploreList.getHandlerToPage(exploreListHandler,pageName)
        explorePage.launchPage(elHandler)
        logger.debug('Page Launched : %s',pageName)
        return configmanager
    except ValueError:
        return ValueError

def getHandlesForEachComponent(driver, driverHelper, configManager, pageName):
    listOfHandles = {}
    for eachComp in configManager.screenComponentRelations[pageName]:
        for comp in configManager.componentChildRelations[eachComp]:
                # locator = (configManager.componentSelectors[comp]['selector'],configManager.componentSelectors[comp]['locator'],configManager.componentSelectors[comp]['wait'])
            locator = (configManager.componentSelectors[comp]['selector'],configManager.componentSelectors[comp]['locator'])
            try:
                wait = configManager.componentSelectors[comp]['wait']
                listOfHandles[comp] = driverHelper.waitForVisibleElements(locator,False)
            except:
                listOfHandles[comp] = driverHelper.waitForVisibleElements(locator)
    return listOfHandles

def getScreenInstance(driver,pageName):
    '''
    Need Generic Implementation
    :param driver:
    :param pageName:
    :return:
    '''

    if "site" in pageName:
        return SitePageClass(driver)

def testScreen(driver,driverHelper,pageName):
    try:
        # Config Parsing Part
        data = {}
        configManager = launchPage(driver,driverHelper,pageName)
        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName)
        screenInstance = getScreenInstance(driver,pageName)
        btvData = screenInstance.btv.getData(handles)
        data['btvData'] = {}
        for key,value in btvData.iteritems():
            pv = value.pop(0)
            if len(data['btvData']) == 0:
                data['btvData']['dimension'] = value
            else:
                data['btvData']['value'] = value
            logger.debug('Col1 : %s  and Col2 : %s',key,value)
        data['btvSelection'] = screenInstance.btv.getSelection(handles)
        for key,value in data['btvSelection'].iteritems():
            logger.debug('Selection : %s ',value)
        screenInstance.btv.setSelection(4,handles)
        logger.info("Setting index --> 4")
        data['btvSelection'] = screenInstance.btv.getSelection(handles)
        for key,value in data['btvSelection'].iteritems():
            logger.debug('Selection : %s ',value)
        data['btvTooltipData'] = screenInstance.btv.getToolTipInfo(driver,driverHelper,handles)
        for i in range(0,len(data['btvTooltipData'])):
            logger.debug('Tooltip %s : %s ',i,data['btvTooltipData'][i])
        result = screenInstance.btv.validateToolTipData(data)
        for key,value in result.iteritems():
            logger.debug('DIMENSION : %s  and RESULT : %s',key,value)






    except ValueError:
        return ValueError





def testBTV(driver,driverHelper):
    try:
        sitePage = SitePageClass(driver)
        btvLocators = sitePage.btv.getSpecificLocators(BTVLocators)
        btvHandlers = driverHelper.waitForVisibleElementsAndChilds(btvLocators)
        return sitePage.btv.getSelectionIndex(btvHandlers)
        # return sitePage.btv.totalCheck(btvHandlers)
    except ValueError:
        return ValueError


def getBTVData(driver,driverHelper):
    try:
        sitePage = SitePageClass(driver)

        btvLocators = sitePage.btv.getSpecificLocators(BTVLocators)
        btvHandlers = driverHelper.waitForVisibleElementsAndChilds(btvLocators)
        data = sitePage.btv.getData(btvHandlers)
        for key,value in data.iteritems():
            logger.debug('Col1 : %s  and Col2 : %s',key,value)
        return data
    except ValueError:
        return ValueError

def drilltoScreen(driver,driverHelper,pageName):
    try:
        sitePage = SitePageClass(driver)
        cmLocators = sitePage.cm.getSpecificLocators(CommonElementLocators)
        cmHandlers = driverHelper.waitForVisibleElementsAndChilds(cmLocators)
        sitePage.cm.activateContextMenuOptions(cmHandlers)

        cmenuLocators = sitePage.cm.getSpecificLocators(ContextMenuLocators)
        cmenuHandlers = driverHelper.waitForVisibleElementsAndChilds(cmenuLocators)
        sitePage.cm.drillTo(driver,driverHelper,cmenuHandlers,Constants.DRILLTO)

        drillLocators = sitePage.cm.getSpecificLocators(DrillToLocators)
        drillHandlers = driverHelper.waitForVisibleElementsAndChilds(drillLocators)
        sitePage.cm.drillTo(driver,driverHelper,drillHandlers,Constants.VRF)

        logger.debug('Page Launched : %s',Constants.VRF)
        return True


    except ValueError:
        return ValueError