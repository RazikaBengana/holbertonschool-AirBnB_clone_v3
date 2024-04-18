#!/usr/bin/python3
"""Script to perform unit testing for the console module of the HBNB project"""

import console
import inspect
import pep8
import unittest


HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Test cases for checking the documentation and PEP8 conformance of the console module"""

    def test_pep8_conformance_console(self):
        """Test if console.py is PEP8 compliant"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test if tests/test_console.py is PEP8 compliant"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Ensure the console module has a comprehensive docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Ensure the HBNBCommand class within the console module has a comprehensive docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
