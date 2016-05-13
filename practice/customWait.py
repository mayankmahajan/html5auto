from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def waitForElementPresence(type,str,timeOut,driver):
    xpath = '//*[contains(@' + type + ', "' + str +'")]'
    WebDriverWait(driver, timeOut).until(EC.presence_of_element_located((By.XPATH, xpath)))

def waitForElement_to_be_visible(type,str,timeOut,driver):
    xpath = '//*[contains(@' + type + ', "' + str +'")]'
    WebDriverWait(driver, timeOut).until(EC.visibility_of_element_located((By.XPATH, xpath)))

def waitForElement_to_be_clickable(type,str,timeOut,driver):
    xpath = '//*[contains(@' + type + ', "' + str +'")]'
    WebDriverWait(driver, timeOut).until(EC.element_to_be_clickable((By.XPATH, xpath)))