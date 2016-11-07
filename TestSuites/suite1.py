import glob

test_file_strings = glob.glob('../Tests/test_*.py')
module_strings = [str.split('/')[1] + "." + str.split('/')[2].split('.')[0] for str in test_file_strings]
[__import__(str) for str in module_strings]






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