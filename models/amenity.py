#!/usr/bin/python
"""
This module defines the Amenity class which is part of a larger models module;
This class represents the Amenity entity in the application, supporting both database and non-database storage options
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    This class provides the structure for storing amenities in the application's database,
    functioning with SQLAlchemy ORM to map to a database table,
    or defaulting to simple attribute storage when no database is used
    """

    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

    else:
        name = ""  # Establish a default attribute when no database is available

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the Amenity class,
        setting up both inherited properties from BaseModel and Base classes and any Amenity-specific initialization
        """
        super().__init__(*args, **kwargs)
