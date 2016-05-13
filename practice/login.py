import customWait


def login(username,password,driver):
    customWait.waitForElementPresence('id', 'username', 30, driver)
    username = driver.find_element_by_id('username').send_keys(username)
    customWait.waitForElementPresence('id', 'password', 30, driver)
    password = driver.find_element_by_id('password').send_keys(password)
    sButton = driver.find_element_by_css_selector('[ng-click = "vm.login()"]')
    sButton.click()