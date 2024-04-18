#!/usr/bin/python3
"""
This module serves as a base for other classes in this ORM framework;
Handles initialization, updates, and serialization of model instances
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid


# Standard format for datetime representation in this model
time = "%Y-%m-%dT%H:%M:%S.%f"


if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object  # Use a plain object if not using a database


class BaseModel:
    """Base class for all models, supporting initialization, and state management"""

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new instance or updates an existing one based on a dictionary of attributes"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()

            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()

            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Provide a string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Save the instance to the storage, updating 'updated_at' timestamp"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance attributes to a dictionary for serialization, handling datetime conversion"""
        new_dict = self.__dict__.copy()

        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)

        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict

    def delete(self):
        """Remove the instance from storage"""
        models.storage.delete(self)
