#!/usr/bin/python3
"""This module handles operations related to states and cities within a storage system"""

import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Class that represents a state entity, and handles different storage methodologies"""

    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the State class"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """Return a list of City instances related to the State if not using a database"""
            city_list = []
            all_cities = models.storage.all(City)

            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list
