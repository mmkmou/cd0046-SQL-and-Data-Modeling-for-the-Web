from itertools import count
from ntpath import join
from unicodedata import name
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from sqlalchemy import and_, cast, func, Date
from datetime import date
from controllers.ArtistController import artists
from models.models import Artist, Show, Venue, db
from forms import *

# Venues List controller
# This function return all venues group by city and State
#----------------------------------------------------------------------------#
def venues():
  # Get All City And State from menu 
  #----------------------------------------------------------------------------#
  locations = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  data = list()
   
  # Return All venue by City & State 
  #----------------------------------------------------------------------------#
  for location in locations:
    venues = Venue.query.with_entities(Venue.id, Venue.name, func.count(Show.id)
      ).join(Show, and_(Show.venue_id == Venue.id, cast(Show.start_time,Date) >  date.today()), isouter=True
      ).filter(Venue.city == location[0]
      ).filter(Venue.state == location[1]
      ).group_by(Venue.id, Venue.name
      ).all()

    data.append( {
      "city": location.city,
      "state": location.state,
      "venues" : venues
    })
    
  return render_template('pages/venues.html', areas=data)

# search on artists with partial case-insensitive  string.
# -------------------------------------------------------------------# 
def search_venues():
  
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  data = Venue.query.with_entities(Venue.id.label("id"), Venue.name.label("name"), func.count(Show.id).label("num_upcoming_shows")
                ).join(Show, and_(Show.venue_id == Venue.id, cast(Show.start_time,Date) >  date.today()), isouter=True
                ).filter(Venue.name.ilike(search)
                ).group_by(Venue.id, Venue.name
                ).all()


  response = {
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

# Show Venue detail page controller
#----------------------------------------------------------------------------#
def show_venue(venue_id):
  data = Venue.query.get(venue_id).__dict__
  
  past_shows = Show.query.with_entities(Show.artist_id.label("artist_id"), Artist.name.label("artist_name"),
                                        Artist.image_link.label("artist_image_link"), Show.start_time.label("start_time")
                                       ).filter_by(venue_id=venue_id
                                       ).join(Artist
                                       ).filter(cast(Show.start_time,Date) <  date.today()
                                       ).all()
                                       
  data["past_shows"] = past_shows
  data["past_shows_count"] = len(past_shows)
   
  
  upcoming_shows = Show.query.with_entities(Show.artist_id.label("artist_id"), Artist.name.label("artist_name"),
                                            Artist.image_link.label("artist_image_link"), Show.start_time.label("start_time")
                                           ).filter_by(venue_id=venue_id
                                           ).join(Artist
                                           ).filter(cast(Show.start_time,Date) >=  date.today()
                                           ).all()

  
  
  data["upcoming_shows"] = upcoming_shows
  data["upcoming_shows_count"] = len(upcoming_shows)
  
  return render_template('pages/show_venue.html', venue=data)

def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('venue.show_venue', venue_id=venue_id))
