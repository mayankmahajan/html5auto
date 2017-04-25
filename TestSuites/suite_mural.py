import glob
from Utils.logger import *
from Utils.resultlogger import *
import os
import platform
from Utils.send_mail_1 import *

def appendTestCase(module):
    pass_count = 0
    fail_count = 0
    for tc in testcases:
        if tc['status'] == "FAIL":
            fail_count=fail_count+1
        elif tc['status'] == "PASS":
            pass_count=pass_count+1

    testcases.append(pass_count)
    testcases.append(fail_count)
    testsuite[module] = testcases

def dump_to_html(testsuite):
    with open(result_chart_file_path,"a") as f:
        f.write("<table>")
        f.write("<tr>")
        f.write("<td>"+str("Testcase")+"</td>")
        f.write("<td>"+str("Status")+"</td>")
        f.write("<td>"+str("Expected Result")+"</td>")
        f.write("<td>"+str("Actual Result")+"</td>")
        f.write("</tr>")
        for suite,testcases in testsuite.iteritems():
            f.write(str(suite))
            f.write("<table>")
            f.write("<tr>")
            f.write("<td>"+str("Testcase")+"</td>")
            f.write("<td>"+str("Status")+"</td>")
            f.write("<td>"+str("Expected Result")+"</td>")
            f.write("<td>"+str("Actual Result")+"</td>")
            f.write("</tr>")
            for i in range(len(testcases)-2):
                # if testcases[i]['status'] == "FAIL":
                f.write("<tr>")
                f.write("<td>"+str(testcases[i]['title'])+"</td>")
                f.write("<td><font color='red'>"+str(testcases[i]['status'])+"</font></td>")
                f.write("<td>"+str(testcases[i]['expected'])+"</td>")
                f.write("<td>"+str(testcases[i]['actual'])+"</td>")
                # for k,v in testcases[i].iteritems():
                #     f.write("<td>"+str(v)+"</td>")
                f.write("</tr>")
            f.write("</table>")
            f.write("<br><br>")


    suites = testsuite.keys()
    failCounts = []
    passCounts = []
    for i in range(len(suites)):
        failCounts.append(testsuite[suites[i]][len(testsuite[suites[i]])-1])
        passCounts.append(testsuite[suites[i]][len(testsuite[suites[i]])-2])

    text_to_dump = "Highcharts.chart('container', {chart: {type: 'bar'},title: {text: 'Test Results'},xAxis: {categories: " \
                   +str(suites)+ \
                   "},yAxis: {min: 0,title: {text: 'TestCase Numbers'}},legend: {reversed: true},plotOptions: {series: {stacking: 'normal'}}," \
                   "series: [{name: 'Fail',data: " \
                   +str(failCounts)+ \
                   "}," \
                   "{name: 'Pass',data: " \
                   +str(passCounts)+ \
                   "}]});"
    return text_to_dump

    # with open("/Users/mayank.mahajan/Downloads/Archive-3/js_1.js","w") as f:
    #     global js_file_path
    #     # js_file_path = os.path.abspath("../logs/js_1.js")
    #     js_file_path = "js_1.js"
    #     f.write(text_to_dump)

    # return text_to_dump


if platform.system() == "Windows":
    delimiter = "\\"
else:
    delimiter = "/"

test_file_strings = glob.glob('../dummytest_screens_bulkstats/test_*.py')

# creating global object accessed through out all modules
import __builtin__
__builtin__.testcases = []
testsuite = {}

# creating Chart File
global result_chart_file_path
result_chart_file_path = '../logs/result_chart_'+time.strftime("%d_%m_%y_%H_%M_%S")+'.html'
logger.info("Chart File Path ========= %s",str(result_chart_file_path))

with open('../logs/result_chart_'+time.strftime("%d_%m_%y_%H_%M_%S")+'.html',"w") as f:
    f.write("")
result_chart_file_path = os.path.abspath(result_chart_file_path)


module_strings = [module.split(delimiter)[1] + "." + module.split(delimiter)[2].split('.')[0] for module in test_file_strings]

for module in module_strings:
    try:
        testcases = []
        logger.debug('*********** TestCase Start ***********')
        resultlogger.debug('<br>*********** Logging Results for %s ***********<br>', module)
        logger.debug('Executing TestCase %s', module)
        __import__(module)
        appendTestCase(module)
        logger.debug('*********** TestCase End (%s) ***********', module)
        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
            print os.system("taskkill /im chrome.exe /f")
            logger.debug('ChromeBrowser killed by taskkill /im chrome.exe /f')

        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"', e)
            try:
                logger.debug('Executing  "taskkill /im chrome.exe /f"')
                print os.system("taskkill /im chrome.exe /f")
            except:
                logger.error('Got Exception %s while executing "taskkill /im chrome.exe /f"', e)
    except Exception as e:
        appendTestCase(module)
        # driver.save_screenshot('screenshots/screenie.png')
        logger.error('Exception found while executing %s ::: %s', module, e)
        logger.debug('*********** TestCase (%s) End with Exceptions ***********', module)
        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"',e)


text_to_dump  = dump_to_html(testsuite)
with open(result_chart_file_path) as f:
    data = f.readlines()
    # sendmail_selenium(additional_script_path=js_file_path,additional_text=data[0])
    sendmail_selenium(additional_script_path=text_to_dump,additional_text=data[0])