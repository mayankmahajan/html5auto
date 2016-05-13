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
import unittest
from validateData import validateData
import page

class sitePage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://nrmca.guavus.com:6443/")

    def tearDown(self):
        driver = self.driver
        driver.close()
        # self.driver.quit()


    def test_driverTitle(self):
        driver = self.driver
        assert "NR-MCA" in driver.title

    def test_Data(self):
        driver = self.driver
        login('admin','Admin@123',driver)
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


        sLabels = driver.find_elements_by_class_name('selectionLabel')
        sLabel = [eachLabel.text for eachLabel in sLabels if eachLabel.location['x'] > 300]

        driver.find_element_by_id('dl-menucontextMenuDisplay').click()
        waitForElement_to_be_visible("id","frameworkDrill",10,driver)
        driver.find_element_by_id('frameworkDrill').click()
        waitForElement_to_be_visible("id","NWT_FUNC_SCR",10,driver)
        driver.find_element_by_id("NWT_FUNC_SCR").click()

        waitForElement_to_be_visible("id","pieView",30,driver)
        assert 'BRANCHBURGNJWDC' in sLabel


if __name__ == '__main__':
    unittest.main()