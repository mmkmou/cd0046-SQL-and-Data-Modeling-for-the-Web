#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import logging
from logging import Formatter, FileHandler

from sqlalchemy import desc

from utils import format_datetime
from models.models import db, Venue, Artist
from routes.venue import venue
from routes.artist import artist
from routes.show import show


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
csrf.exempt(venue)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

app.jinja_env.filters['datetime'] = format_datetime


#  Front Page
#  ----------------------------------------------------------------
@app.route('/')
def index():
    venues  = Venue.query.with_entities(Venue.id, Venue.name).order_by(desc(Venue.id)).limit(10).all()
    artists  = Artist.query.with_entities(Artist.id, Artist.name).order_by(desc(Artist.id)).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)

#  Venues
#  ----------------------------------------------------------------
app.register_blueprint(venue, url_prefix='/venues')

#  Artists
#  ----------------------------------------------------------------
app.register_blueprint(artist, url_prefix='/artists')

#  Shows
#  ----------------------------------------------------------------
app.register_blueprint(show, url_prefix='/shows')

#  error Handler
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

