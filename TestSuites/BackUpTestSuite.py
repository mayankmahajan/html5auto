import unittest
from scripts.logger import logger

from TestCases.TestCase1 import TestCase1
from TestCases.TestCase2 import TestCase2


class TestSuite(unittest.TestCase):
    def test_suite(self):
        self.suite = unittest.TestSuite()

        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(TestCase1),
            unittest.defaultTestLoader.loadTestsFromTestCase(TestCase2)
        ])
        runner = unittest.TextTestRunner()

        logger.info("Test Suite Initiated")

        runner.run(self.suite)

if __name__ == "__main__":
    unittest.main(exit=False)

