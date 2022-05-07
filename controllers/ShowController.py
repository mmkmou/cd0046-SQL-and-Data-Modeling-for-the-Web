from tokenize import String
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from datetime import datetime, timezone
from models.models import Show, Venue, Artist
from forms import *

# displays list of shows at /shows
#----------------------------------------------------------------------------#
def shows():
  data = Show.query.with_entities(Show.venue_id.label("venue_id"), Venue.name.label("venue_name"),
                                  Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), 
                                  Artist.image_link.label("artist_image_link"), Show.start_time.label("start_time")
  ).join(Venue
  ).join(Artist
  ).all()

  return render_template('pages/shows.html', shows=data)

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
