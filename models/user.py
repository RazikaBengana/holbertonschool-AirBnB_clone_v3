#!/usr/bin/python3
"""This module models a User object within the system, integrating both database and non-database storage mechanisms"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Representation of a User object,
    defining database schema and relationships for the 'users' table when using a database,
    or simple attributes when not
    """

    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")  # Relationship to places associated with the user
        reviews = relationship("Review", backref="user")  # Relationship to reviews written by the user

    # Default fields if not using a database
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new user instance with optional arguments and keyword arguments"""
        super().__init__(*args, **kwargs)
