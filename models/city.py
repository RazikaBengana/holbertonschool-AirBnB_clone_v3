#!/usr/bin/python
"""
This module provides classes and functions for handling cities in a database
or a simple storage mechanism, depending on the configuration
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    Representation of a city in the application;
    This class can interact with a database if configured to do so,
    or it can operate with simple attribute storage
    """

    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")

    else:
        state_id = ""  # State ID if not using a database
        name = ""  # City name if not using a database

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the City class"""
        super().__init__(*args, **kwargs)
