#!/usr/bin/python3
"""
This script initializes the 'models' package by setting up storage options based on an environment variable;
It supports two types of storage: 'db' (database) and file-based storage
"""

from os import getenv


# Retrieving the type of storage from the environment variable 'HBNB_TYPE_STORAGE'
storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    # Import DBStorage class from the models.engine.db_storage module
    from models.engine.db_storage import DBStorage
    # Create an instance of DBStorage
    storage = DBStorage()

else:
    # Import FileStorage class from the models.engine.file_storage module
    from models.engine.file_storage import FileStorage
    # Create an instance of FileStorage
    storage = FileStorage()

# Call the reload method on the storage instance which loads data from the storage
storage.reload()

