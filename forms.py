from datetime import datetime
from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional, Regexp
from markupsafe import escape

from models.models_enum import State, Genre, coerce_for_enum

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(v, v.value) for v in State],
        coerce=coerce_for_enum(State)    
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[
            Optional(),
            Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message="Invalid phone number format : xxx-xxx-xxxx")
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[(v, v.value) for v in Genre],
        coerce=coerce_for_enum(Genre)
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    website_link = StringField(
        'website_link'
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = TextAreaField(
        'seeking_description'
    )

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(v, v.value) for v in State],
        coerce=coerce_for_enum(State)
    )
    phone = StringField(
        'phone', validators=[
            Optional(),
            Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', message="Invalid phone number format : xxx-xxx-xxxx")
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[(v, v.value) for v in Genre],
        coerce=coerce_for_enum(Genre)
     )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
     )

    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = TextAreaField(
            'seeking_description'
     )

