#!/usr/bin/python3
"""
Script to perform unit testing for the FileStorage class within a storage handling system,
particularly focusing on file-based storage
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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


FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Test cases for the documentation and style of the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Gather all functions of the FileStorage class for further testing of documentation"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that the file_storage.py conforms to PEP8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test that tests for file_storage.py conforms to PEP8"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test the existence of module docstring in file_storage.py"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test the existence of the docstring for FileStorage class"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test the existence of docstrings in all functions of the FileStorage class"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Define tests for the functionalities of the FileStorage class"""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all method returns a dictionary of objects"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test that new method correctly adds objects to the storage dictionary"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}

        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save method correctly saves all objects to file.json"""
        storage = FileStorage()
        new_dict = {}

        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save

        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)

        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get method returns object based on class and id"""
        FileStorage._FileStorage__objects = {}
        storage = FileStorage()
        state = State()
        storage.new(state)
        storage.save()
        state2 = storage.get(State, state.id)
        self.assertEqual(state.id, state2.id)

        # test without a valid class
        result = storage.get(None, state.id)
        self.assertEqual(result, None)

        # test without a valid id
        result = storage.get(State, "this is not a valid ID")
        self.assertEqual(result, None)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count method returns the count of objects by class type"""
        FileStorage._FileStorage__objects = {}
        storage = FileStorage()
        city = City()
        storage.new(city)
        city2 = City()
        storage.new(city2)
        state = State()
        storage.new(state)
        user = User()
        storage.new(user)
        user2 = User()
        storage.new(user2)
        storage.save()

        self.assertEqual(2, storage.count(City))
        self.assertEqual(1, storage.count(State))
        self.assertEqual(2, storage.count(User))

        os.remove("file.json")
