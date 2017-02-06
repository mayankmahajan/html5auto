import glob
from Utils.logger import *
from Utils.resultlogger import *
import os
import platform

if platform.system() == "Windows":
    delimiter = "\\"
else:
    delimiter = "/"

test_file_strings = glob.glob('../suitemural*/test_*.py')

# module_strings = [str.split('/')[1] + "." + str.split('/')[2].split('.')[0] for str in test_file_strings]
module_strings = [str.split(delimiter)[1] + "." + str.split(delimiter)[2].split('.')[0] for str in test_file_strings]
# [__import__(str) for str in module_strings]


for str in module_strings:
    try:
        logger.debug('*********** TestCase Start ***********')
        resultlogger.debug('<br>*********** Logging Results for %str ***********<br>',str)
        logger.debug('Executing TestCase %s', str)
        __import__(str)
        logger.debug('*********** TestCase End (%s) ***********', str)
        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"', e)

    except Exception as e:
        # driver.save_screenshot('screenshots/screenie.png')
        logger.error('Exception found while executing %s ::: %s',str,e)
        logger.debug('*********** TestCase (%s) End with Exceptions ***********', str)
        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"',e)




# import unittest
# testSuite = unittest.TestSuite()
# suites = [unittest.TestLoader().loadTestsFromName(str) for str in module_strings]
# [testSuite.addTest(suite) for suite in suites]
# print testSuite
#
# result = unittest.TestResult()
# testSuite.run(result)
# print result
#
# Ok, at this point, I have a result, how do I display it as the normal unit test
# command line output?
# if __name__ == "__main__":
#     unittest.main()