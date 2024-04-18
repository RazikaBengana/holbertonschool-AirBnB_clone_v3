#!/usr/bin/python
"""
This module manages the interaction between the application and the database specifically for 'Place' related operations;
It includes the definition of the Place model and conditional creation of database tables depending on the storage type
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


# Conditionally define the 'place_amenity' table if storage type is database
if models.storage_t == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))

class Place(BaseModel, Base):
    """Model representation of a Place object, including attributes like city, user, and descriptions"""

    if models.storage_t == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of Place with optional arguments"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """Return a list of Review instances associated with this Place if not using database storage"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)

            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)

            return review_list

        @property
        def amenities(self):
            """Return a list of Amenity instances associated with this Place if not using database storage"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)

            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)

            return amenity_list
