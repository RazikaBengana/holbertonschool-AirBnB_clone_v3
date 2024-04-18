#!/usr/bin/python3
"""This module initializes various models and their storage handling"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# Dictionary linking class names to their respective classes
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Class for serializing instances to a JSON file and deserializing JSON file to instances"""

    __file_path = "file.json"  # path to the JSON file
    __objects = {}  # dictionary to store all objects by <class name>.<id>

    def all(self, cls=None):
        """
        Return a dictionary of all objects;
        Optionally, filter objects by class
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict

        return self.__objects

    def new(self, obj):
        """Add an object to the storage dictionary"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def get(self, cls, id):
        """
        Retrieve one object based on the class and its ID;
        Return None if no object found
        """
        from models import storage
        if cls or id:
            for objects in storage.all(cls).values():
                if objects.id == id:
                    return objects
        else:
            return None

    def count(self, cls=None):
        """
        Count the number of objects in storage;
        Optionally, filter by class
        """
        if cls:
            return len(self.all(cls))

    def save(self):
        """Serialize the objects to the JSON file specified by __file_path"""
        json_objects = {}

        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()

        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserialize the JSON file to objects, if file exists;
        Catch and ignores errors if file doesn't exist
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """Delete an object from storage if it exists"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id

            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
