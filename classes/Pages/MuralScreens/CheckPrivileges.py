from classes.Pages.ExplorePageClass import *
from Utils.utility import *
from classes.Components.DropdownComponentClass import *

class CheckPrivileges(BasePageClass):

    def __init__(self,driver):
        '''
        Constructor
        '''
        self.driver = driver
        self.dropdown = DropdownComponentClass()
        BasePageClass.__init__(self,driver)

    def checkWorkflows(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        checkEqualAssert(True, exploreScreenInstance.exploreList.launchModule(exploreHandle, "WORKFLOWS"), '', '',"Verify Workflows Privileges")
        return

    def checkDPIAlerts(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        if exploreScreenInstance.exploreList.launchModule(exploreHandle, "ALERTS"):
            isError(setup)
            checkEqualAssert(True,self.dropdown.clickSpanWithTitle("DPI Alerts",getHandle(setup, MuralConstants.ALERTSCREEN, Constants.ALLSPANS)),"","","Verify DPI Alerts Privileges")
            return
        else:
            checkEqualAssert(True,exploreScreenInstance.exploreList.launchModule(exploreHandle, "ALERTS"),"","","Verify DPI Alerts")


    def checkReports(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        checkEqualAssert(True,exploreScreenInstance.exploreList.launchModule(exploreHandle, "REPORTS"),'','',"Verify Reports Privileges")
        return

    def checkBulkstatsKPI(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        exploreScreenInstance.exploreList.switchApp(exploreHandle)
        h=getHandle(setup, "explore_Screen")
        list=exploreScreenInstance.exploreList.getAllApps(h)

        if "Bulkstats / KPIs" in list:
            URL=setup.d.current_url
            value=str(URL).split('/')[len(str(URL).split('/'))-1]
            if value =='bulkstats':
                checkEqualAssert(True,value,'','','Verify Bulkstats KPI Privileges')
            else:
                result = exploreScreenInstance.exploreList.launchappByName(getHandle(setup, "explore_Screen"),"Bulkstats / KPIs")
                time.sleep(3)
                setup.d.switch_to.window(setup.d.window_handles[2])
                time.sleep(5)
                setup.d.close()
                setup.d.switch_to.window(setup.d.window_handles[1])
                checkEqualAssert(True,result,'','','Verify Bulkstats KPI Privileges')
        else:
            checkEqualAssert(True,"Bulkstats / KPIs" in list,'','','Verify Bulkstats KPI Privileges')


    def checkKPIAlerts(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        if exploreScreenInstance.exploreList.launchModule(exploreHandle, "ALERTS"):
            isError(setup)
            checkEqualAssert(True, self.dropdown.clickSpanWithTitle("KPI Alerts",getHandle(setup, MuralConstants.ALERTSCREEN,Constants.ALLSPANS)), "", "","Verify KPI Alerts Privileges")
            return
        else:
            checkEqualAssert(True,exploreScreenInstance.exploreList.launchModule(exploreHandle, "ALERTS"),"","","Verify KPI Alerts")

    def checkUserManagement(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        exploreScreenInstance.exploreList.switchApp(exploreHandle)
        h = getHandle(setup, "explore_Screen")
        list = exploreScreenInstance.exploreList.getAllApps(h)

        if "User Management" in list:
            result = exploreScreenInstance.exploreList.launchappByName(getHandle(setup, "explore_Screen"),"User Management")
            time.sleep(5)
            setup.d.switch_to.window(setup.d.window_handles[2])
            time.sleep(5)
            setup.d.close()
            setup.d.switch_to.window(setup.d.window_handles[1])
            checkEqualAssert(True, result, '', '', 'Verify User Management Privileges')
        else:
            checkEqualAssert(True, "User Management" in list, '', '', 'Verify User Management Privileges')


    def checkSystemMonitoring(self,setup):
        exploreScreenInstance = ExplorePageClass(setup.d)
        exploreHandle = getHandle(setup, "explore_Screen")
        exploreScreenInstance.exploreList.switchApp(exploreHandle)
        h = getHandle(setup, "explore_Screen")
        list = exploreScreenInstance.exploreList.getAllApps(h)

        if "System Monitoring Interface" in list:
            result = exploreScreenInstance.exploreList.launchappByName(getHandle(setup, "explore_Screen"),"System Monitoring Interface")
            time.sleep(5)
            setup.d.switch_to.window(setup.d.window_handles[2])
            time.sleep(5)
            setup.d.close()
            setup.d.switch_to.window(setup.d.window_handles[1])
            checkEqualAssert(True, result, '', '', 'Verify System Monitoring Interface Privileges')
        else:
            checkEqualAssert(True,"System Monitoring Interface" in list, '', '', 'Verify System Monitoring Interface Privileges')
