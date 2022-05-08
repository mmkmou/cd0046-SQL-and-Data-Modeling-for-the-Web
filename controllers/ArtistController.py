from datetime import date
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from sqlalchemy import Date, and_, cast, func
from models.models import Artist, Show, Venue
from forms import *

# Artist List controller
# This function return all artist
#----------------------------------------------------------------------------#
def artists():
  data  = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)


# search on artists with partial case-insensitive  string.
# -------------------------------------------------------------------# 
def search_artists():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  data = Artist.query.with_entities(Artist.id.label("id"), Artist.name.label("name"), func.count(Show.id).label("num_upcoming_shows")
                ).join(Show, and_(Show.artist_id == Artist.id, cast(Show.start_time,Date) >=  date.today()), isouter=True
                ).filter(Artist.name.ilike(search)
                ).group_by(Artist.id, Artist.name
                ).all()


  response = {
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


# Show Artist detail page controller
#----------------------------------------------------------------------------#
def show_artist(artist_id):

  data = Artist.query.get(artist_id).__dict__
  past_shows = Show.query.with_entities(Show.venue_id.label("venue_id"), Venue.name.label("venue_name"),
                                        Venue.image_link.label("venue_image_link"), Show.start_time.label("start_time")
                                       ).filter_by(artist_id=artist_id
                                       ).join(Venue
                                       ).filter(cast(Show.start_time,Date) <  date.today()
                                       ).all()
                                       
  data["past_shows"] = past_shows
  data["past_shows_count"] = len(past_shows)
   
  
  upcoming_shows = Show.query.with_entities(Show.venue_id.label("venue_id"), Venue.name.label("venue_name"),
                                            Venue.image_link.label("venue_image_link"), Show.start_time.label("start_time")
                                            ).filter_by(artist_id=artist_id
                                            ).join(Venue
                                            ).filter(cast(Show.start_time,Date) >=  date.today()
                                            ).all()

  
  
  data["upcoming_shows"] = upcoming_shows
  data["upcoming_shows_count"] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)


def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('artist.show_artist', artist_id=artist_id))

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

