from tokenize import String
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from datetime import datetime, timezone
from models.models import Show, Venue, Artist, db
from forms import ShowForm

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

# Show Create page controller 
#----------------------------------------------------------------------------#
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

# Show Create submission page controller 
#----------------------------------------------------------------------------#
def create_show_submission():
  show =  ShowForm()
  try: 
    if show.validate_on_submit():
          record = Show(
              artist_id = request.form['artist_id'],
              venue_id = request.form['venue_id'],
              start_time = request.form['start_time']
          )
          
          db.session.add(record)
          db.session.commit()
          # on successful db insert, flash success
          flash('Show was successfully listed!')
    else:
          for field, errors in show.errors.items():
              for error in errors:
                  
                  flash("Error in {}: {}".format(
                      getattr(show, field).label.text,
                      error
                  ), 'error')
  except Exception as error:
    flash(str(error.orig) + " for parameters" + str(error.params), 'error')
    
  return redirect(url_for('index', ))

