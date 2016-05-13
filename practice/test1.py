from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from copy import deepcopy
from customWait import waitForElementPresence
from customWait import waitForElement_to_be_visible
from customWait import waitForElement_to_be_clickable
from login import login


def launchBrowser(browserName):
    return webdriver.Firefox()

# def login(username,password,driver):
#     waitForElementPresence('id','username',30)
#     username = driver.find_element_by_id('username').send_keys(username)
#     waitForElementPresence('id','password',30)
#     password = driver.find_element_by_id('password').send_keys(password)
#     sButton = driver.find_element_by_css_selector('[ng-click = "vm.login()"]')
#     sButton.click()

# def waitForElementPresence(type,str,timeOut,driver):
#     xpath = '//*[contains(@' + type + ', "' + str +'")]'
#     WebDriverWait(driver, timeOut).until(EC.presence_of_element_located((By.XPATH, xpath)))
#
# def waitForElement_to_be_visible(type,str,timeOut,driver):
#     xpath = '//*[contains(@' + type + ', "' + str +'")]'
#     WebDriverWait(driver, timeOut).until(EC.visibility_of_element_located((By.XPATH, xpath)))
#
# def waitForElement_to_be_clickable(type,str,timeOut,driver):
#     xpath = '//*[contains(@' + type + ', "' + str +'")]'
#     WebDriverWait(driver, timeOut).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def validateData(data,parQuetFilePath):
    d = deepcopy(data)
    with open(parQuetFilePath,'r') as open_file:
        dataRead  = [eachline.strip('\n') for eachline in open_file.readlines()]
        print 'Data Read from CSV : ', dataRead

if __name__ == '__main__':
    driver  = launchBrowser('xyz')
    driver.maximize_window()

    # assertion
    driver.get("https://nrmca.guavus.com:6443/")
    assert "NR-MCA" in driver.title
    login('admin','Admin@123',driver)

    # Printing Explore Options

    waitForElementPresence("id","exploreLabel",30,driver)
    exploreLabels = driver.find_elements_by_xpath('//*[contains(@id, "exploreLabel")]')
    for i in range(len(exploreLabels)):
        if exploreLabels[i].text == 'Sites':
            exploreLabels[i].click()
            break

    # Goto Sites and get BarTabularView Data
    waitForElement_to_be_clickable("id",'YESTERDAY',30,driver)
    driver.find_element_by_id('YESTERDAY').click()
    waitForElement_to_be_visible("id","_barTabularView",30,driver)

    waitForElementPresence("class","column1rowStyle",30,driver)
    bar = driver.find_element_by_xpath('//*[contains(@id, "_barTabularView")]')
    column1 = bar.find_elements(by=By.XPATH,value='//*[contains(@class, "column1")]')
    column2 = bar.find_elements(by=By.XPATH,value='//*[contains(@class, "column2")]')

    a=[el1.text for el1 in column1]
    b=[el2.text for el2 in column2]
    print a
    print b

    validateData(b,'dumped1.csv')

    waitForElement_to_be_clickable('id','TODAY',30,driver)
    driver.find_element_by_id('TODAY').click()
    # driver.implicitly_wait(20)

    waitForElement_to_be_visible("id","_barTabularView",30,driver)
    newbar = driver.find_element_by_xpath('//*[contains(@id, "_barTabularView")]')
    newcolumn1 = newbar.find_elements(by=By.XPATH,value='//*[contains(@class, "column1")]')
    newcolumn2 = newbar.find_elements(by=By.XPATH,value='//*[contains(@class, "column2")]')

    print [nel1.text for nel1 in newcolumn1]
    print [nel2.text for nel2 in newcolumn2]

    # driver.find_element_by_css_selector('[title="BURBANKCAWDC"]').click()
    driver.find_element_by_css_selector('[title="BRANCHBURGNJWDC"]').click()

    driver.find_element_by_id('dl-menucontextMenuDisplay').click()
    waitForElement_to_be_visible("id","frameworkDrill",10,driver)
    driver.find_element_by_id('frameworkDrill').click()
    waitForElement_to_be_visible("id","NWT_FUNC_SCR",10,driver)
    driver.find_element_by_id("NWT_FUNC_SCR").click()

    waitForElement_to_be_visible("id","pieView",30,driver)

    driver.close()
    driver.quit()