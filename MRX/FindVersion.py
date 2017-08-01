from Utils.SetUp import *
from classes.Pages.MRXScreens.UDScreenClass import *
from classes.Pages.ExplorePageClass import *
version = ''
def find_VersionFromUI(screenName,parent='alllabels',child='label'):
    h=getHandle(setup,screenName)
    for i in range(len(h[parent][child])):
        if 'ersion' in h[parent][child][i].text:
            return str(h[parent][child][i+1].text).strip(']')
    return "Not_Found"

try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    exploreScreenInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, "explore_Screen")
    if exploreScreenInstance.exploreList.clickOnHelpIcon(exploreHandle,parent='appHeader',child='helpIcon'):
        if exploreScreenInstance.exploreList.launchModule(getHandle(setup, "explore_Screen"),'About'):
            version=find_VersionFromUI("AboutUs_Screen")

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
