import unittest
from Utils.logger import *

from Tests.Test1 import *
from Tests.Test2 import *
from Tests.Test3 import *
from Tests.Test4 import *
from Tests.Test5 import *
from Tests.Test6 import *
from Tests.Test7 import *

class TestSuite(unittest.TestCase):

    def test_suite(self):
        self.suite = unittest.TestSuite()

        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Test1),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test2),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test3),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test4),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test5),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test6),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test7)
        ])
        runner = unittest.TextTestRunner()

        # logger.info("Test Suite Initiated")

        # runner.run(self.suite)

if __name__ == "__main__":

    logger.info("Test Suite Initiated")
    unittest.main(exit=False)

