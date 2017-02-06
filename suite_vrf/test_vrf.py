from Utils.SetUp import *
from Utils.utility import *
from classes.Pages.VrfPageClass import *

#######################################################################
# Getting Setup Details
setup = SetUp()
#######################################################################


#######################################################################
#get time range and measures from config file
timeIteration = len(setup.cM.getNodeElements("quicklinks","quicklink"))
quicklinks = setup.cM.getNodeElements("quicklinks","quicklink").keys()
t=0

measureIteration = len(setup.cM.getNodeElements("measures","measure"))
measures = setup.cM.getNodeElements("measures","measure").keys()
#######################################################################

#######################################################################
# Logging into the appliction and launch site screen
login_status=login(setup, "admin", "Admin@123")
checkEqualAssert(True,login_status,"","","Login to NRMCA UI")
exploreScreenInstance = ExplorePageClass(setup.d)
exploreHandle = getHandle(setup,"explore_Screen")
launch_status = exploreScreenInstance.exploreList.launchScreen(exploreHandle,"exploreList","site_Screen")

checkEqualAssert(True,launch_status,"","","launch site screen")
sleep(5)
#######################################################################


#######################################################################
# get screen instance and set timerange and measure and Get the handles of the screen
set_measure=measures[0]
set_time=quicklinks[0]
screenInstance = SitePageClass(setup.d)
setTimeRange(setup,set_time)
siteScreenHandle = getHandle(setup,"site_Screen")
screenInstance.measure.doSelection(siteScreenHandle, set_measure)
#######################################################################

#######################################################################
# Get the default selection and Validate the result
test_case1="Default selection of site screen"
siteScreenHandle = getHandle(setup,"site_Screen")
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
checkEqualAssert(str(1),str(defSelection['selIndex']),set_time,set_measure,test_case1)
#######################################################################


#######################################################################
# Set the bar Table view to the 2 index and validate the result
a = screenInstance.btv.setSelection(2,siteScreenHandle)
defSelection = screenInstance.btv.getSelection(siteScreenHandle)
data=screenInstance.btv.getData(siteScreenHandle)
status=drilltoScreen(setup.d,setup.dH,Constants.VRF)
test_case2 ="Drill TO VRF Screen"
checkEqualAssert("True",str(status),set_time,set_measure,test_case2)
#######################################################################

#######################################################################
#Create screen instance and get handle of screen
vrfScreenInstance = VrfPageClass(setup.d)
vrfScreenHandle = getHandle(setup,Constants.VRF)
#######################################################################


#######################################################################
VAR=vrfScreenInstance.switcher.getSelection(vrfScreenHandle)
test_case3="Default Selection in chart"
checkEqualAssert("Chart",str(VAR),set_time,set_measure,test_case3)
#######################################################################


#######################################################################
# Get the default selection of vrf screen
deflegendSel = vrfScreenInstance.btv.getSelection(vrfScreenHandle)
test_case4="Default Selection of btv in VRF screen"
checkEqualAssert(str(1),str(deflegendSel['selIndex']),set_time,set_measure,test_case4)
#######################################################################

#######################################################################
#Check single selection on btv
Selection_list=[2] # for multiple selection put more items in list
for i in Selection_list:
    vrfScreenInstance.btv.setSelection(i,vrfScreenHandle)
    vrfScreenHandle = getHandle(setup,Constants.VRF)
    deflegendSel = vrfScreenInstance.btv.getSelection(vrfScreenHandle)
    test_case5="Check Selection of btv in VRF screen"

    checkEqualAssert(str(i),str(deflegendSel['selIndex']),set_time,set_measure,test_case5)
#######################################################################

#######################################################################
#Get chart data and tooltip data
piedata = vrfScreenInstance.btv.getData(vrfScreenHandle)
#csvreader = CSVReader()
#result = screenInstance.btv.validateBTVData(data,csvreader.csvData)
#print result
#######################################################################


#######################################################################
#measuse and time range selection and data validation
while t < timeIteration:
    i=0
    set_time=quicklinks[t]
    setTimeRange(setup,quicklinks[t])

    # while loop is to iterate over all the measure
    while i < measureIteration:
        print measures[i]
        set_measure=measures[i]
        logger.debug("selecting measure : %s", measures[i])
        screenInstance.measure.doSelection(vrfScreenHandle, measures[i])
        vrfScreenHandle = getHandle(setup, Constants.VRF)
        btvdata=screenInstance.btv.getData(vrfScreenHandle)
        data['btvData'] = {}
        for key, value in btvdata.iteritems():
            pv = value.pop(0)
            if len(data['btvData']) == 0:
                data['btvData']['dimension'] = value
            else:
                data['btvData']['value'] = value
            logger.debug('Col1 : %s  and Col2 : %s', key, value)

        data['btvTooltipData']=screenInstance.btv.getToolTipInfo(setup.d, setup.dH,vrfScreenHandle)
        result1 = screenInstance.btv.validateToolTipData1(data)
        validatemessage = "Match tooltip data and btv data"

        checkEqualAssert(result1, True, quicklinks[t], measures[i], validatemessage)

        i+=1
    t+=1

#######################################################################


#######################################################################
#search box testing on vrf screen
vrfScreenHandle = getHandle(setup,Constants.VRF)
data1=vrfScreenInstance.btv.getData(vrfScreenHandle)
text=["p","","cd",Keys.BACK_SPACE,"@","$","*","&","-","_"]
click=["one","two"]
count=1
for word in text:
    if word==Keys.BACK_SPACE:
       index_previous = text.index(Keys.BACK_SPACE) - 1
       word1 = text[text.index(Keys.BACK_SPACE) - 1][:-1]
       msg = "Search_for_Backspace "
       setSearch = vrfScreenInstance.searchComp.setSearchText(vrfScreenHandle, text[index_previous])
    else:
        word1=word
        msg = "Search_for_" + word + " "
    expected_search_result=[data1["BTVCOLUMN1"][j] for j in range(2,len(data1["BTVCOLUMN1"])) if data1["BTVCOLUMN1"][j].lower().find(word1.lower()) >= 0]
    setSearch = vrfScreenInstance.searchComp.setSearchText(vrfScreenHandle,word)
    time.sleep(5)
    if(setSearch==True):
     for click_times in click:
        if click_times == "one":
            vrfScreenInstance.searchComp.hitSearchIcon(vrfScreenHandle)
        elif click_times == "two" and count==1:
            vrfScreenInstance.searchComp.hitSearchIcon(vrfScreenHandle)
            vrfScreenInstance.searchComp.hitSearchIcon(vrfScreenHandle)
            expected_search_result = data1["BTVCOLUMN1"][2::]
            count=0
        else:
            break
        vrfScreenHandle = getHandle(setup, Constants.VRF)
        search_pie_result=vrfScreenInstance.btv.getData(vrfScreenHandle)
        print search_pie_result
        checkEqualAssert(expected_search_result, search_pie_result["BTVCOLUMN1"][2::],set_time,set_measure, msg+str(click_times)+" time")
        vrfScreenInstance.searchComp.hitSearchIcon(vrfScreenHandle)
    else:
     checkEqualAssert(False, setSearch,set_time,set_measure, "word_not_set_for_"+word)

setup.d.close()
######################################################################