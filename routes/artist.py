from flask import Blueprint
from controllers.ArtistController import *

artist = Blueprint('artist', __name__)

artist.route('/')(artists)
artist.route('/search', methods=['POST'])(search_artists)
artist.route('/<int:artist_id>')(show_artist)
artist.route('/<int:artist_id>/edit', methods=['GET'])(edit_artist)
artist.route('/<int:artist_id>/edit', methods=['POST'])(edit_artist_submission)
artist.route('/create', methods=['GET'])(create_artist_form)
artist.route('/create', methods=['POST'])(create_artist_submission)
