import unittest
from Utils.logger import *

from Tests.Test1 import *
from Tests.Test2 import *
from Tests.Test3 import *

class TestSuite(unittest.TestCase):

    def test_suite(self):
        self.suite = unittest.TestSuite()

        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Test1),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test2),
            unittest.defaultTestLoader.loadTestsFromTestCase(Test3)
        ])
        runner = unittest.TextTestRunner()

        logger.info("Test Suite Initiated")

        # runner.run(self.suite)

if __name__ == "__main__":

    unittest.main(exit=False)

