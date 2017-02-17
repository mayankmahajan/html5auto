#!/usr/bin/env python
##############################################################
'''
Called Directly from TestCase
'''
__author__      = "Mayank Mahajan"
__email__       = 'mayank.mahajan@guavus.com'
__version__     = "1.0"
__maintainer__  = "Mayank Mahajan"
##############################################################


from Utils.logger import *
from Utils.resultlogger import *
from classes.DriverHelpers.locators import *
from classes.Pages import ExplorePageClass
from classes.Pages.LoginPageClass import *
from classes.Pages.ExplorePageClass import *
from classes.Pages.SitePageClass import *
from classes.Pages.NEPageClass import *
from classes.Pages.MRX_SegmentPageClass import *
from classes.DriverHelpers.DriverHelper import *
from Utils.ConfigManager import ConfigManager
from copy import deepcopy
from Utils.csvReader import CSVReader
from classes.Components.ContextMenuComponentClass import *
from classes.Components.BaseComponentClass import *
import time
import datetime
import calendar
from classes.Pages.GenerateReportsPopClass import *
from classes.Pages.ReportsModuleClass import *
from classes.Objects.Report import *

# def setUp():
#     obj={}
#     obj.d = webdriver.Chrome('/Users/mayank.mahajan/Downloads/chromedriver')
#     obj.d.get(Constants.URL)
#     obj.dH = DriverHelper(obj.d)
#     obj.cM = ConfigManager()
#     return obj

def setupTestcase(self):
    self.driver = webdriver.Firefox()
    self.driverHelper = DriverHelper(self.driver)
    return True

def checkEqualDict(f1,f2,time="",measure="",message=""):
    msg = time + " " + measure + " " + message
    tcPass = "<b><font color='green'> PASS</font></b><br>"
    tcFail = "<b><font color='red'> FAIL</font></b><br>"
    for k,v in f1.iteritems():
        try:
            assert f1[k] == f2[k]
            # msg = msg+" : "+k+" "+tcPass
            resultlogger.info(msg+" : "+k+" "+tcPass)
            logger.info(msg+" : "+k+" "+tcPass)

        except AssertionError :

            # msg = msg+" Expected: "+str(f1[k])+" Actual: "+str(f2[k])+tcFail
            resultlogger.info(msg+" Expected: "+str(f1[k])+" Actual: "+str(f2[k])+tcFail)
            logger.info(msg+" Expected: "+str(f1[k])+" Actual: "+str(f2[k])+tcFail)
        except KeyError:
            resultlogger.info(msg+" Expected: "+str(f1[k])+" Actual: key not present :"+str(k)+tcFail)
            logger.info(msg+" Expected: "+str(f1[k])+" Actual: key not present :"+str(k)+tcFail)

def checkEqualAssert(f1,f2,time="",measure="",message=""):
    msg = time + " " + measure + " " + message
    tcPass = "<b><font color='green'> PASS</font></b><br>"
    tcFail = "<b><font color='red'> FAIL</font></b><br>"
    try:
        assert f1 == f2
        msg = msg+tcPass
        resultlogger.info(msg)
        logger.info(msg)

    except AssertionError:

        msg = msg+" Expected: "+str(f1)+" Actual: "+str(f2)+tcFail
        resultlogger.info(msg)
        logger.info(msg)



def login(obj,username,password):
    try:
        driver = obj.d
        driverHelper = obj.dH
        configmanager = obj.cM
        # configmanager = ConfigManager()
        # configmanager = configmanager
        configs = configmanager.componentSelectors
        # configs = configmanager.getComponentConfigs()
        loginConfigs = deepcopy(configs)

        usernameHandler = driverHelper.waitForVisibleElement((loginConfigs['username']['username']['selector'],loginConfigs['username']['username']['locator']))
        passwordHandler = driverHelper.waitForVisibleElement((loginConfigs['password']['password']['selector'],loginConfigs['password']['password']['locator']))
        signinHandler = driverHelper.waitForVisibleElement((loginConfigs['signin']['signin']['selector'],loginConfigs['signin']['signin']['locator']))

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

def launchPage(obj,pageName,isStartScreen=False):
    try:
        driver = obj.d
        driverHelper = obj.dH
        configmanager = obj.cM
        explorePage = ExplorePageClass(driver)
        # exploreListHandler = driverHelper.waitForVisibleElements(ExplorePageLocators.EXPLORELIST)
        # elHandler = explorePage.exploreList.getHandlerToPage(exploreListHandler,pageName)

        # configmanager = ConfigManager()
        # screenConfigs = deepcopy(configmanager.getScreenConfigs())
        screenConfigs = deepcopy(configmanager.componentSelectors)
        componentConfigsPerScreen = deepcopy(configmanager.getComponentConfigsPerScreen('exploreScreen'))

        # locator = (screenConfigs['sites']['selector'],screenConfigs['sites']['locator'])
        locator = (screenConfigs[pageName]['selector'],screenConfigs[pageName]['locator'])
        # locator = (screenConfigs[''])
        elHandler = driverHelper.waitForVisibleElement(locator)
        # elHandler = explorePage.exploreList.getHandlerToPage(exploreListHandler,pageName)
        explorePage.launchPage(elHandler)
        logger.debug('Page Launched : %s',pageName)
        # sleep(4)
        return True
    except Exception:
        return Exception

def getHandlersForParentComponent(driver, driverHelper, configManager, pageName,parent="NA"):
    listOfHandles = {}
    if parent == "NA":
        parents = configManager.screenComponentRelations[pageName]
    else:
        parents = [parent]
    for comp in parents:
        if configManager.screenSelectors[pageName][comp]['parent'].upper() == "TRUE":
            locator = (configManager.screenSelectors[pageName][comp]['selector'],configManager.screenSelectors[pageName][comp]['locator'])
            try:
                wait = configManager.screenSelectors[pageName][comp]['wait']
                listOfHandles[comp] = driverHelper.waitForVisibleElements(locator,False)
            except:
                # try:
                #     isParent = True if configManager.componentSelectors[eachComp][comp]['parent'].upper() == "TRUE" else False
                # except:
                #     pass
                listOfHandles[comp] = driverHelper.waitForVisibleElements(locator)

    return listOfHandles

def getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles,parent="NA"):
    listOfHandles = {}
    if parent == "NA":
        parents = configManager.screenComponentRelations[pageName]
    else:
        parents = [parent]
    for eachComp in parents:
        print "getHandlesForEachComponent",eachComp
        listOfHandles[eachComp] = {}
        for comp in configManager.componentChildRelations[eachComp]:
                # locator = (configManager.componentSelectors[eachComp][comp]['selector'],configManager.componentSelectors[eachComp][comp]['locator'],configManager.componentSelectors[eachComp][comp]['wait'])
            locator = (configManager.componentSelectors[eachComp][comp]['selector'],configManager.componentSelectors[eachComp][comp]['locator'])
            try:
                wait = configManager.componentSelectors[eachComp][comp]['wait']
                try:
                    print "will not wait for ", comp
                    if configManager.componentSelectors[eachComp][comp]['locatorDimension']:
                        locatorDimension = configManager.componentSelectors[eachComp][comp]['locatorDimension']
                        locatorText = configManager.componentSelectors[eachComp][comp]['locatorText']
                        try:
                            parentDependency = configManager.componentSelectors[eachComp][comp]['parentDependency']
                            listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,False,[parentHandles,eachComp],comp,locatorDimension,locatorText,parentDependency)
                        except:
                            listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,False,[parentHandles,eachComp],comp,locatorDimension,locatorText)
                except:
                        listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,False,[parentHandles,eachComp],comp)

            except:
                # try:
                #     isParent = True if configManager.componentSelectors[eachComp][comp]['parent'].upper() == "TRUE" else False
                # except:
                #     pass
                try:
                    print "will wait for ", comp
                    if configManager.componentSelectors[eachComp][comp]['locatorDimension']:
                        locatorDimension = configManager.componentSelectors[eachComp][comp]['locatorDimension']
                        locatorText = configManager.componentSelectors[eachComp][comp]['locatorText']
                        if 'parentDependency' in configManager.componentSelectors[eachComp][comp].keys():
                            listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,True,[parentHandles,eachComp],comp,locatorDimension,locatorText,configManager.componentSelectors[eachComp][comp]['parentDependency'])
                        else:
                            listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,True,[parentHandles,eachComp],comp,locatorDimension,locatorText)
                except:
                    listOfHandles[eachComp][comp] = driverHelper.waitForVisibleElements(locator,True,[parentHandles,eachComp],comp)
    return listOfHandles

def getScreenInstance(driver,pageName):
    '''
    Need Generic Implementation
    :param driver:
    :param pageName:
    :return:
    '''

    # if "site" in pageName:
    return SitePageClass(driver)

def testScreen1(driver,driverHelper,pageName,isStartScreen=False,componentList=[]):
    try:
        # Config Parsing Part
        data = {}
        if isStartScreen:
            configManager = launchPage(driver,driverHelper,pageName)
        else:
            configManager = ConfigManager()
        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)
        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)
        screenInstance = getScreenInstance(driver,pageName)
        # testing Table

        logger.debug("SwitcherCard Selection : %s",screenInstance.switcher.getSelection(handles))
        screenInstance.switcher.setSelection(1,handles)  # 0 -> Chart and 1 -> Table
        logger.debug("SwitcherCard Selection : %s",screenInstance.switcher.getSelection(handles))

        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)
        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)
        # screenInstance.scrollToElement(driver,handles)
        # if 'siteInteraction_Screen' in pageName:
        print screenInstance.table.getData(driver,handles)
        print screenInstance.table.sortTable(driver,handles,"Total Tonnage(%)")

        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)
        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)

        screenInstance.table.getSortedColumn(driver,handles)



        # driver.execute_script("return arguments[0].scrollIntoView();", handles['ROWS'][len(handles['ROWS'])-1])




    except ValueError:
        return ValueError

def merge_dictionaries(d1,d2):
    n = d1.copy()
    n.update(d2)
    return n

def getTableDataMap(setup,screenName,parent='table',colIndex=0):
    reportScreenInstance = ReportsModuleClass(setup.d)
    tableHandle = getHandle(setup,screenName,parent)
    return reportScreenInstance.table.getTableDataMap(tableHandle, parent, setup,colIndex)


def isError(setup):
    eHandle = getHandle(setup,Constants.ERRORPOPUP,Constants.ERRORBODY)
    if len(eHandle[Constants.ERRORBODY][Constants.ERRORCLOSE]) >0:
        logger.error("Error Pop Up found")
        errorMessage = eHandle[Constants.ERRORBODY][Constants.ERRORMESSAGE][0].text
        logger.error("Error Pop Up Message = %s",errorMessage)
        logger.debug("Closing Error Pop Up")
        eHandle[Constants.ERRORBODY][Constants.ERRORCLOSE][0].click()
        try:
            eHandle[Constants.ERRORBODY][Constants.ERRORCLOSE][0].click()
        except:
            pass

        return [True,errorMessage]
    else:
        return [False,""]


def getHandle(obj,pageName,parent="NA"):
    '''
    Takes out handler of the Page along with components
    :param obj:
    :param pageName:
    :return:
    '''
    driver = obj.d
    driverHelper = obj.dH
    configmanager = obj.cM
    # screenInstance=getScreenInstance(obj.d,pageName)
    parentHandles = getHandlersForParentComponent(driver,driverHelper,configmanager,pageName,parent)
    handles = getHandlesForEachComponent(driver, driverHelper, configmanager, pageName, parentHandles,parent)
    # time.sleep(2)
    return handles


def testScreen(obj,pageName,isStartScreen=False):
    driver = obj.d
    driverHelper = obj.dH
    configManager = obj.cM

    try:
        # Config Parsing Part
        data = {}
        if isStartScreen:
            launchPage(obj,pageName)
        else:
            configManager = ConfigManager()
        # tempString = '//*[contains(@id, "' + pageName.split('_')[0]+'_barTabularView")]'
        # configManager.componentSelectors['btv']['locator'] = tempString
        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)

        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)

        # getting site and component instances will be moved from here.
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
        screenInstance.btv.setSelection(3,handles)
        logger.info("Setting index --> 3")
        data['btvSelection'] = screenInstance.btv.getSelection(handles)
        for key,value in data['btvSelection'].iteritems():
            logger.debug('Selection : %s ',value)
        data['btvTooltipData'] = screenInstance.btv.getToolTipInfo(driver,driverHelper,handles)
        for i in range(0,len(data['btvTooltipData'])):
            logger.debug('Tooltip %s : %s ',i,data['btvTooltipData'][i])

        # #####
        # Need to comment if not run

        result1 = screenInstance.btv.validateToolTipData(data)
        for key,value in result1.iteritems():
            logger.debug('DIMENSION : %s  and RESULT : %s',key,value)
        #
        # csvreader = CSVReader()
        # result2 = screenInstance.btv.validateBTVData(data,csvreader.csvData)
        # logger.info("********* Logging Data Validation Results *********")
        # for key,value in result2.iteritems():
        #     logger.debug('DIMENSION : %s  and RESULT : %s',key,value)

        # #####

        # testing Table

        screenInstance.switcher.getSelection(handles)  # 0 -> Chart and 1 -> Table
        screenInstance.switcher.setSelection(1,handles)  # 0 -> Chart and 1 -> Table






    except ValueError:
        return ValueError




def dummy_testScreen(driver,driverHelper,pageName,isStartScreen=False):
    try:
        # Config Parsing Part
        data = {}
        if isStartScreen:
            configManager = launchPage(driver,driverHelper,pageName)
        else:
            configManager = ConfigManager()
        # tempString = '//*[contains(@id, "' + pageName.split('_')[0]+'_barTabularView")]'
        # configManager.componentSelectors['btv']['locator'] = tempString
        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)

        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)

        screenInstance = getScreenInstance(driver,pageName)
        measure="Flows"
        screenInstance.measure.doSelection(handles,measure)
        return True





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
        try:
            sitePage.cm.drillTo(driver,driverHelper,cmenuHandlers,Constants.DRILLTO)
        except Exception:
            return Exception

        drillLocators = sitePage.cm.getSpecificLocators(DrillToLocators)
        drillHandlers = driverHelper.waitForVisibleElementsAndChilds(drillLocators)

        if(sitePage.cm.drillTo(driver,driverHelper,drillHandlers,pageName) == True):
            pass
        else:
            return sitePage.cm.drillTo(driver,driverHelper,drillHandlers,pageName)

        # time.sleep(3)

        logger.debug('Page Launched : %s',pageName)
        return True


    except ValueError:
        return ValueError


def exportTo(driver,driverHelper,pageName):
    try:
        sitePage = SitePageClass(driver)
        cmLocators = sitePage.cm.getSpecificLocators(CommonElementLocators)
        cmHandlers = driverHelper.waitForVisibleElementsAndChilds(cmLocators)
        sitePage.cm.activateContextMenuOptions(cmHandlers)

        cmenuLocators = sitePage.cm.getSpecificLocators(ContextMenuLocators)
        cmenuHandlers = driverHelper.waitForVisibleElementsAndChilds(cmenuLocators)
        try:
            sitePage.cm.drillTo(driver,driverHelper,cmenuHandlers,Constants.EXPORTTO)
        except Exception:
            return Exception

        exportLocators = sitePage.cm.getSpecificLocators(ExportToLocators)
        exportHandlers = driverHelper.waitForVisibleElementsAndChilds(exportLocators)

        if(sitePage.cm.drillTo(driver,driverHelper,exportHandlers,pageName) == True):
            pass
        else:
            return sitePage.cm.drillTo(driver,driverHelper,exportHandlers,pageName)

        # time.sleep(3)

        logger.debug('Page Launched : %s',pageName)
        return True


    except ValueError:
        return ValueError








def mrxSegmentScreen(driver,driverHelper,pageName,isStartScreen=False):
    try:
        # Config Parsing Part
        data = {}
        if isStartScreen:
            configManager = launchPage(driver,driverHelper,pageName)
        else:
            configManager = ConfigManager()
        # tempString = '//*[contains(@id, "' + pageName.split('_')[0]+'_barTabularView")]'
        # configManager.componentSelectors['btv']['locator'] = tempString
        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)

        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)

        # getting site and component instances will be moved from here.
        screenInstance = MRX_SegmentPageClass(driver)
        # testing Table

        print screenInstance.table.getData(driver,handles)
        print screenInstance.table.sortTable(driver,handles,"Status")
    except ValueError:
        return ValueError


def testPie(driver,driverHelper,pageName,isStartScreen=False,componentList=[]):
    try:
        parentHandles = getHandlersForParentComponent(driver,driverHelper,configManager,pageName)
        handles = getHandlesForEachComponent(driver, driverHelper, configManager, pageName, parentHandles)

        screenInstance = getScreenInstance(driver,pageName)
        # testing pie

        print screenInstance.pielegend.getData(handles)
        print screenInstance.pielegend.getSelection(handles)
        print screenInstance.pielegend.setSelection(4,handles)
        print screenInstance.pielegend.getSelection(handles)

    except ValueError:
        return ValueError



def setTimeRange(obj,quicklink,pageName="site_Screen"):
    '''
    sets quicklinks on the particular page
    :param obj:
    :param quicklink:
    :param pageName:
    :return:
    '''
    driver = obj.d
    driverHelper = obj.dH
    configmanager = obj.cM
    screenInstance=getScreenInstance(obj.d,pageName)

    parentHandles = getHandlersForParentComponent(driver,driverHelper,configmanager,pageName)
    handles = getHandlesForEachComponent(driver, driverHelper, configmanager, pageName, parentHandles)

    screenInstance.quiklinkTimeRange.setSelection(quicklink,handles)

def setMeasure(obj,measure,pageName):
    '''
    sets quicklinks on the particular page
    :param obj:
    :param quicklink:
    :param pageName:
    :return:
    '''
    driver = obj.d
    driverHelper = obj.dH
    configmanager = obj.cM
    screenInstance=getScreenInstance(obj.d,pageName)

    parentHandles = getHandlersForParentComponent(driver,driverHelper,configmanager,pageName)
    handles = getHandlesForEachComponent(driver, driverHelper, configmanager, pageName, parentHandles)

    result = screenInstance.measure.doSelection(handles,measure)

    return result

def setSiteType(obj,sites,screenInstance,handles):
    # driver = obj.d
    # driverHelper = obj.dH
    # configmanager = obj.cM
    # screenInstance = getScreenInstance(obj.d,pageName)
    # parentHandles = getHandlersForParentComponent(driver,driverHelper,configmanager,pageName)
    # handles = getHandlesForEachComponent(driver,driverHelper,configmanager,pageName,parentHandles)

    screenInstance.measure.doSelectionSite(handles,sites)





def parseBTVData(btvData):
    data  = {}
    data['btvData'] = {}
    for key,value in btvData.iteritems():
        pv = value.pop(0)
        if len(data['btvData']) == 0:
            data['btvData']['dimension'] = value
        else:
            data['btvData']['value'] = value
        logger.debug('Col1 : %s  and Col2 : %s',key,value)
    return  data['btvData']



def getSummaryBarData(measure,btvname,screenInstance,siteScreenHandle):
    values = measure.split('_')

    try:
        if (values[3]=="average"):
            values[3]="Average"
    except:
        print "Average is not there"

    try:
        if (values[3]=="peak"):
            values[3]="Peak"

    except:
        print "Peak is not there"

    if (values[0]=="Wan-Cost($)"):
        values[0] = "Wan Cost($)"
        selections = screenInstance.summarybar.getSelection(siteScreenHandle)
        #print "hahaha"
        #print selections['All WDC']
        summarybarvalues = selections[btvname][values[0]]['Average']
        return summarybarvalues

    else:
        selections = screenInstance.summarybar.getSelection(siteScreenHandle)
        #print selections[btvname]
        summarybarvalues = selections[btvname][values[0]][values[3]]
        return summarybarvalues


def IsreportIDvalid(data):
    result = True
    for key,value in data.iteritems():
        print value
    if 'rows' in key:
        for a in value:
            print a[0]
            # i = i + 1
            for b in value[1:]:
                print b[0]
                if (a[0]==b[0]):
                    result = False
                    break;
                else:
                    result = True
            break;
    return result

def currentdate():
    x = datetime.datetime.now()
    # print x
    y =str(x).split(':')
    date = y[0]+":"+y[1]
    # print y
    # print date
    return date

def validatesearchtable(data,columnname,searchtext):
    try:
        flag = False
        for j in range(len(data['header'])):
            if(data['header'][j].upper()==columnname.upper()):
                col = j
                break;
        flag = False
        for i in range(len(data['rows'])):
            if(searchtext in data['rows'][i][col]):
                print data['rows'][i][col]
                flag = True
            else:
                flag = False
        return flag
    except:
        return False


def setCalendar(y,m,d,h,min,intance,setup,page="routers_popup",parent="leftcalendar"):
    try:
        intance.calendar.set("year",y,getHandle(setup,page,parent),parent)
        intance.calendar.set("month",m,getHandle(setup,page,parent),parent)
        intance.calendar.setDay("day",d,getHandle(setup,page,parent),parent)
        intance.calendar.set("hour",h,getHandle(setup,page,parent),parent)
        try:
            intance.calendar.set("minute",min,getHandle(setup,page,parent),parent)
        except:
            pass
        return True
    except ElementNotSelectableException or ElementNotVisibleException or Exception as e:
        return e


def getInputText(h,parent,child):
    for el in h[parent][child]:
        if el.is_displayed() == True:
            return el.get_attribute("value")


def FindWordInString(ar,grPopHandle):
    resultq = []
    for el in ar:
        if (el in grPopHandle['generateReportDialog']['filters'][0].text):
            result ="True"
        else:
            result = "False"

        resultq = result
    if (all(value == "True" for value in resultq)):
        flag = True
    else:
        flag = False
    return flag

# def getAbsolutePath(filename):

def getepoch(datestring,tOffset=Constants.TIMEZONEOFFSET,tPattern=Constants.TIMEPATTERN):
    epoch = int(calendar.timegm(time.strptime(datestring.strip()+":00",tPattern)))
    return epoch - tOffset*3600

def getDateString(epoch,tOffset=Constants.TIMEZONEOFFSET,tPattern=Constants.TIMEPATTERN):
    tuple = time.gmtime(epoch+tOffset*3600)
    return time.strftime(tPattern,tuple)



def createreport(setup,reportType,reportObj,time):
    '''
    takes input as reporttype,time,filters,reportName,other optional params
    :return:
    '''

    # creating a random number
    rndmNum = random.randint(0,999999)


    inputinfo={}
    inputinfo['reporttype'] = reportType['id']
    inputinfo['timerange'] = reportType['locatorText']
    inputinfo['starttime'] = time[0].datestring
    inputinfo['endtime'] = ''
    # inputinfo['endtime'] = time[1].datestring
    inputinfo['email'] = reportObj.email
    inputinfo['reportname'] = reportObj.reportName+str(rndmNum)

    reportScreenInstance = ReportsModuleClass(setup.d)
    reportScreenInstance.launchCreateReport1(setup.d)

    grPopInstance = GenerateReportsPopClass(setup.d)
    grPopInstance.reportspopup.selectRadioButton(inputinfo['reporttype'], getHandle(setup,"report2_popup","radios"), "label")

    # launching TimeRange Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))

    # selecting quicklink
    r = grPopInstance.reportspopup.selectRadioButton(inputinfo['timerange'], getHandle(setup,"report2_popup","radios"), "label")
    logger.error("%s RadioButton not Found", inputinfo['timerange']) if r == False else ""


    grPopHandle = getHandle(setup, "report2_popup", "generateReportDialog")


    if 'starttime' in reportType.keys() and reportType['starttime'] == "True":
        grPopHandle['generateReportDialog']['starttime'][0].click()
        setCalendar(time[0].year, time[0].month, time[0].day, time[0].hour, time[0].min, grPopInstance, setup,"report2_popup")
        grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, "report2_popup", "allbuttons"))

    # print "starttime", str(getInputText(grPopHandle,'generateReportDialog','starttime'))
    if 'endtime' in reportType.keys() and reportType['endtime'] == "True":
        grPopHandle['generateReportDialog']['endtime'][0].click()
        setCalendar(time[1].year, time[1].month, time[1].day, time[1].hour, time[1].min, grPopInstance, setup,"report2_popup")
        grPopInstance.reportspopup.clickButton("Apply", getHandle(setup, "report2_popup", "allbuttons"))


    # print "endtime", str(getInputText(grPopHandle,'generateReportDialog','endtime'))
    if 'recurringInterval' in reportType.keys() and reportType['recurringInterval'] != "":
        grPopInstance.dropdown.doSelection(getHandle(setup,"report2_popup","recurring"),reportType['recurringInterval'],"recurring","dropdowns")

    if 'recurInstances' in reportType.keys() and reportType['recurringInterval'] != "":
        grPopInstance.dropdown.customSendkeys(getHandle(setup,"report2_popup","recurring")['recurring']["instances"],reportType['recurInstances'])

    # getting info from TimeRange Page

    inputinfo['starttime'] = grPopInstance.dropdown.getValue_input(getHandle(setup, "report2_popup", "allinputs"),0)

    if 'ourly' not in reportType['locatorText'] and 'ecurrring' not in reportType['locatorText']:
        inputinfo['endtime'] = grPopInstance.dropdown.getValue_input(getHandle(setup, "report2_popup", "allinputs"),1)

    # launching Filters Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))


    inputinfo['filters'] = {}
    reportFilters= setup.cM.getNodeElements("reportwizardfilters","filter")

    # for k in reportFilters:
    #     if k in reportType['filters']:

    if 'network' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['network']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['network'])):
            subfilter = ["Area","Region","Gateway"]

            if reportObj.filters['network'][i] != '':
                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['network'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['network'][i],i)
                # inputinfo['filters'].append(['network',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)])
            inputinfo['filters'][subfilter[i]] = grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)


    if 'apnrat' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['apnrat']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['apnrat'])):
            radioname= "APN" if i==0 else "Radio Type"
            if reportObj.filters['apnrat'][i] != '':
                grPopInstance.reportspopup.selectRadioButton(radioname, getHandle(setup,"report2_popup","radios"), "label")

                # grPopInstance.multiDropdown.domultipleSelection(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['apnrat'][i],i)
                grPopInstance.multiDropdown.domultipleSelectionWithIndex(getHandle(setup,"report2_popup","filterPopup"),reportObj.filters['apnrat'][i],i)
                # inputinfo['filters'].append(['apnrat',i,grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)])
                inputinfo['filters'][radioname] = grPopInstance.multiDropdown.getSelection(getHandle(setup,"report2_popup","filterPopup"),i)

    if 'subscriber' in reportType['filters']:
        grPopInstance.clickLink(reportFilters['subscriber']['locatorText'],getHandle(setup, "report2_popup", "alllinks"))
        for i in range(len(reportObj.filters['subscriber'])):
            if reportObj.filters['subscriber'][i] != '':
                grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),0)
                # inputinfo['filters'].append(['subscriber',i,grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, "report2_popup", "allinputs"),1)])
                inputinfo['filters'][reportFilters['subscriber']['locatorText']] = grPopInstance.dropdown.sendkeys_input(reportObj.filters['subscriber'][i],getHandle(setup, "report2_popup", "allinputs"),1)


    # launching Review Page in wizard
    grPopInstance.reportspopup.clickButton("Next Step", getHandle(setup, "report2_popup", "allbuttons"))
    reviewPageParams= {}

    grPopHandle = getHandle(setup, "report2_popup", "generateReportDialog")
    reviewPageParams['filters'] = grPopInstance.getFiltersAtReviewPage(grPopHandle)


    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["reportName"],inputinfo['reportname'])
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),0)
    grPopInstance.dropdown.clickCheckBox(getHandle(setup, "report2_popup", "allcheckboxes"),1)
    grPopInstance.dropdown.customSendkeys(grPopHandle['generateReportDialog']["emailInput"],inputinfo['email'])


    tempArray = [[e.text for e in el.find_elements_by_xpath("*")] for el in grPopHandle['generateReportDialog']['leftBox'][0].find_elements_by_class_name("groupDiv")]


    # reviewPageParams['filters'] = grPopHandle['generateReportDialog']['filters'][0].text

    reviewPageParams['reportname'] = grPopHandle['generateReportDialog']['reportName'][0].get_attribute("value")
    reviewPageParams['email'] = grPopHandle['generateReportDialog']['emailInput'][0].get_attribute("value")
    reviewPageParams['starttime'] = grPopHandle['generateReportDialog']['starttime'][0].get_attribute("value")
    reviewPageParams['endtime'] = grPopHandle['generateReportDialog']['endtime'][0].get_attribute("value")
    reviewPageParams['reporttype'] = tempArray[1][0].split("\n")[1]
    reviewPageParams['timerange'] = tempArray[2][1]

    logger.debug("Report with info is going to be submitted")
    for k,v in reviewPageParams.iteritems():
        logger.debug("%s :: %s.",k,v)

    grPopInstance.reportspopup.clickButton("Submit",getHandle(setup, "report2_popup", "allbuttons"))


    return [inputinfo,reviewPageParams]


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
