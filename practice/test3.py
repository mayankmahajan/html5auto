import unittest

from selenium import webdriver

import page


# import requests

class BaseTestCase(unittest.TestCase):
    pass



class sitePage(BaseTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://nrmca.guavus.com:6443/")

    def tearDown(self):
        self.driver.close()
        # self.driver.quit()

# http://selenium-python.readthedocs.org/page-objects.html
# http://seleniummaster.com/sitecontent/index.php/selenium-web-driver-menu/selenium-test-automation-with-python-menu/241-selenium-python-mvc-multiple-tests-with-unittest-framework

    def test_Sites(self):
        login_page = page.LoginPage(self.driver)
        # Do checks
        assert login_page.is_title_matches(), 'TITLE NOT MATCHED'


        # setattr(login_page,'username','admin')
        login_page.send_username()
        login_page.send_password()
        login_page.click_signIn()
        explore_page = page.ExplorePage(self.driver)
        assert explore_page.is_Site_Available(), 'SITES NOT MATCHED'

    def test_Sites1(self):
        login_page = page.LoginPage(self.driver)
        # Do checks
        assert login_page.is_title_matches(), 'TITLE NOT MATCHED'

        # setattr(login_page,'username','admin')
        login_page.send_username()
        login_page.send_password()
        login_page.click_signIn()
        explore_page = page.ExplorePage(self.driver)
        assert explore_page.is_Site_Available(), 'SITES NOT MATCHED'


if __name__ == '__main__':
    unittest.main()
