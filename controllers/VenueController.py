
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import DateTime, and_, cast, func, Date, true
from datetime import date, datetime
from models.models import Artist, Show, Venue, db
from forms import VenueForm
from utils import format_boolean

# Venues List controller
# This function return all venues group by city and State /venues
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

# search on venue with partial case-insensitive  string. /venues/search
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
                                       ).filter(cast(Show.start_time,DateTime) <  datetime.now()
                                       ).all()
                                       
  data["past_shows"] = past_shows
  data["past_shows_count"] = len(past_shows)
   
  
  upcoming_shows = Show.query.with_entities(Show.artist_id.label("artist_id"), Artist.name.label("artist_name"),
                                            Artist.image_link.label("artist_image_link"), Show.start_time.label("start_time")
                                           ).filter_by(venue_id=venue_id
                                           ).join(Artist
                                           ).filter(cast(Show.start_time,DateTime) >=  datetime.now()
                                           ).all()

  
  
  data["upcoming_shows"] = upcoming_shows
  data["upcoming_shows_count"] = len(upcoming_shows)
  
  return render_template('pages/show_venue.html', venue=data)

# Create Venue page controller [GET] /venue/create
#----------------------------------------------------------------------------#
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

# Subnit Venue creation controller [POST] /venue/create 
#----------------------------------------------------------------------------#
def create_venue_submission():
  venue =  VenueForm()
  try:
    if venue.validate_on_submit():
          record = Venue(
              name = request.form['name'],
              city = request.form['city'],
              state = request.form['state'],
              address = request.form['address'],
              phone = request.form['phone'],
              image_link = request.form['image_link'],
              genres = request.form.getlist('genres'),
              facebook_link = request.form['facebook_link'],
              website_link = request.form['website_link'],
              seeking_talent = format_boolean(request.form.get('seeking_talent', 'n')),
              seeking_description = request.form['seeking_description']
          )
          
          db.session.add(record)
          db.session.commit()
          # on successful db insert, flash success
          flash('Venue ' + request.form['name'] + ' was successfully added!')
    else:
          for field, errors in venue.errors.items():
              for error in errors:
                  
                  flash("Error in {}: {}".format(
                      getattr(venue, field).label.text,
                      error
                  ), 'error')
  except Exception as error:
    flash(str(error.orig) + " for parameters" + str(error.params), 'error')
    
  return render_template('pages/home.html', )


# Delete Venue [GET] /venue/<venue_id>/delete
#----------------------------------------------------------------------------#
def delete_venue(venue_id):
  try:
    Show.query.filter_by(venue_id=venue_id).delete()
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + str(venue_id) + ' was successfully deleted!')
  except Exception as error:
    db.session.rollback()
    flash(str(error.params) + " for parameters" + str(error.params), 'error')
  finally:
    db.session.close()
  
  return redirect(url_for('index', ))

# Edit Venue form page [GET] /venue/<venue_id>/edit
#----------------------------------------------------------------------------#
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

# Edit Venue submissions  [POST] /venue/<venue_id>/edit
#----------------------------------------------------------------------------#
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  try:
    if form.validate_on_submit():
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.image_link = request.form['image_link']
      venue.genres = request.form.getlist('genres')
      venue.facebook_link = request.form['facebook_link']
      venue.website_link = request.form['website_link']
      venue.seeking_talent = format_boolean(request.form.get('seeking_talent', 'n'))
      venue.seeking_description = request.form['seeking_description']

      
      db.session.add(venue)
      db.session.commit()

      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    else:
          for field, errors in venue.errors.items():
              for error in errors:
                  flash("Error in {}: {}".format(
                      getattr(venue, field).label.text,
                      error
                  ), 'error')
  except Exception as error:
    flash(str(error.params) + " for parameters" + str(error.params), 'error')
  return redirect(url_for('venue.show_venue', venue_id=venue_id))



