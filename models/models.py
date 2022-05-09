#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import ARRAY
from flask_sqlalchemy import SQLAlchemy
from models.models_enum import *

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Venue Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(12))
    image_link = db.Column(db.String(500))
    genres = db.Column(MutableList.as_mutable(ARRAY(db.Enum(Genre))), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.Text())
    shows = db.relationship("Show", back_populates="venue")


#----------------------------------------------------------------------------#
# Artist Models.
#----------------------------------------------------------------------------#
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    phone = db.Column(db.String(12))
    image_link = db.Column(db.String(500))
    genres = db.Column(MutableList.as_mutable(ARRAY(db.Enum(Genre))), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.Text())
    shows = db.relationship("Show", back_populates="artist")
    
#----------------------------------------------------------------------------#
# Show Models.
#----------------------------------------------------------------------------#
class Show(db.Model):
    __tablename__ = 'Show'

    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    venue = db.relationship("Venue", back_populates="shows")
    artist = db.relationship("Artist", back_populates="shows")
    __table_args__ = (db.UniqueConstraint('artist_id', 'start_time'),db.UniqueConstraint('venue_id', 'start_time'),)


    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database