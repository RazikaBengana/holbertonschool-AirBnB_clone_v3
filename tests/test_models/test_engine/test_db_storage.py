#!/usr/bin/python3
"""
Script to perform unit testing for the DBStorage class which manages interactions with databases
using models defined in the ORM
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest


DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Test cases for the documentation and PEP8 compliance of DBStorage"""

    @classmethod
    def setUpClass(cls):
        """Set up for test by getting list of functions in DBStorage"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test to ensure that db_storage.py is PEP8 compliant"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test to ensure that the DBStorage test files are PEP8 compliant"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test to check for presence of module docstring in db_storage.py"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test to check for presence of docstring in DBStorage class"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test to ensure all public functions of DBStorage have docstrings"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test cases for file storage specific scenarios"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all method returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all method returns empty when no class is provided"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new method adds new instance to the storage"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save method correctly saves objects to disk"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get method returns the object based on class and id"""

        state = State(name="State test")
        storage.new(state)
        storage.save()
        result = storage.get(State, state.id)
        self.assertEqual(result.id, state.id)
        self.assertEqual(result.created_at, state.created_at)

        result = storage.get(None, state.id)
        self.assertEqual(result, None)

        result = storage.get(State, "this is not a valid ID")
        self.assertEqual(result, None)

        storage.delete(state)
        storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count method returns correct number of objects in storage"""

        total = len(storage.all(State))
        state = State(name="State test")
        storage.new(state)
        storage.save()
        total2 = len(storage.all(State))
        self.assertTrue(total + 1 == total2)
        storage.delete(state)
        storage.save()
