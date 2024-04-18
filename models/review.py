#!/usr/bin/python
"""This module defines models for handling review data with support for different storage types"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """
    A class representing a Review object;
    It is used to create and manage review records in a database;
    The class supports two types of storage: database (db) and non-persistent memory storage
    """

    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)

    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new Review instance;
        The initialization is configured to accept variable arguments (args) and keyword arguments (kwargs),
        allowing for flexibility in instantiation
        """
        super().__init__(*args, **kwargs)
