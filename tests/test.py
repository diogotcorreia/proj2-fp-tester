import unittest
import sys
import importlib
import os
from io import StringIO

target = importlib.import_module(sys.argv[1])

#just a test
class SomeTest(unittest.TestCase):
    def test_example(self):
        """
        Example test
        """
        result = target.some_function()
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
