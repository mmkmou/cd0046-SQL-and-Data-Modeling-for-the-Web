from datetime import date, datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from sqlalchemy import Date, DateTime, and_, cast, func
from models.models import Artist, Show, Venue, db
from forms import ArtistForm
from utils import format_boolean

# Artist List controller
# This function return all artist
#----------------------------------------------------------------------------#
def artists():
  data  = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

# search on artists with partial case-insensitive  string.
#----------------------------------------------------------------------------# 
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
                                       ).filter(cast(Show.start_time,DateTime) <  datetime.now()
                                       ).all()
                                       
  data["past_shows"] = past_shows
  data["past_shows_count"] = len(past_shows)
   
  
  upcoming_shows = Show.query.with_entities(Show.venue_id.label("venue_id"), Venue.name.label("venue_name"),
                                            Venue.image_link.label("venue_image_link"), Show.start_time.label("start_time")
                                            ).filter_by(artist_id=artist_id
                                            ).join(Venue
                                            ).filter(cast(Show.start_time,DateTime) >=  datetime.now()
                                            ).all()

  
  
  data["upcoming_shows"] = upcoming_shows
  data["upcoming_shows_count"] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

# Edit Artist form page [GET] /artist/<artist_id>/edit
#----------------------------------------------------------------------------#
def edit_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

# Edit Artist submissions  [POST] /artist/<artist_id>/edit
#----------------------------------------------------------------------------#
def edit_artist_submission(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()
  try:
    if form.validate_on_submit():
      
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.image_link = request.form['image_link']
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = request.form['facebook_link']
      artist.website_link = request.form['website_link']
      artist.seeking_venue = format_boolean(request.form.get('seeking_venue', 'n'))
      artist.seeking_description = request.form['seeking_description']

      db.session.add(artist)
      db.session.commit()

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    else:
          for field, errors in artist.errors.items():
              for error in errors:
                  
                  flash("Error in {}: {}".format(
                      getattr(artist, field).label.text,
                      error
                  ), 'error')
  except Exception as error:
    flash(str(error.params) + " for parameters" + str(error.params), 'error')

  return redirect(url_for('artist.show_artist', artist_id=artist_id))

# Create Artist page controller [GET] /artist/create
#----------------------------------------------------------------------------#
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# Subnit Venue creation controller [POST] /artist/create 
#----------------------------------------------------------------------------#
def create_artist_submission():

  artist =  ArtistForm()
  try:
    if artist.validate_on_submit():
          record = Artist(
              name = request.form['name'],
              city = request.form['city'],
              state = request.form['state'],
              phone = request.form['phone'],
              image_link = request.form['image_link'],
              genres = request.form.getlist('genres'),
              facebook_link = request.form['facebook_link'],
              website_link = request.form['website_link'],
              seeking_venue = format_boolean(request.form.get('seeking_venue', 'n')),
              seeking_description = request.form['seeking_description']
          )
          
          db.session.add(record)
          db.session.commit()
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
          for field, errors in artist.errors.items():
              for error in errors:
                  
                  flash("Error in {}: {}".format(
                      getattr(artist, field).label.text,
                      error
                  ), 'error')
  except Exception as error:
    flash(str(error.orig) + " for parameters" + str(error.params), 'error')

  return render_template('pages/home.html')