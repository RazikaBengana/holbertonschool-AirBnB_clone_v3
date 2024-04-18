#!/usr/bin/python3
"""
This module manages database interactions for a Flask application,
including the setup and teardown of a database session;
It imports various model classes and initializes a dictionary
of these classes for simplified access and manipulation
"""

import models
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Dictionary mapping class names to classes, simplifying the access to various database models
classes = {"Amenity": Amenity, "City": City, "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    Handles all database operations for the models, including session management, record querying,
    and record lifecycle management from creation to deletion
    """

    __engine = None  # Database engine object, hidden as a private instance attribute
    __session = None  # Scoped session for performing database operations, encapsulated as a private instance attribute

    def __init__(self):
        """
        Initialize a new DBStorage instance, sets up the database engine using configuration from environment variables,
        and optionally drops all tables if running in a testing environment
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve all objects of a specified type or all objects if no type is specified;
        Return the objects in a dictionary where keys are the object class names followed by their IDs
        """
        new_dict = {}

        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Add a new object to the current database session, preparing it for commit"""
        self.__session.add(obj)

    def get(self, cls, id):
        """Retrieve an object by its class and id, or return None if not found"""
        if cls and id:
            for objects in storage.all(cls).values():
                if objects.id == id:
                    return objects
        else:
            return None

    def count(self, cls=None):
        """
        Count the number of objects in storage for a specified class, or count all objects if no class is specified;
        Useful for validation checks and during testing
        """
        if cls:
            return len(self.all(cls))

    def save(self):
        """Commit all changes in the current session to the database, ensuring data consistency"""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete a specified object from the current session, if it exists;
        This operation is reversible only until the session is committed
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Recreate all tables in the database and initializes a new session;
        Useful for ensuring a clean state or during application setup
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Close the current session, freeing resources and locking the current state of the database"""
        self.__session.remove()
