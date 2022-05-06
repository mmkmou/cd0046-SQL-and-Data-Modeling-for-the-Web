from flask import Blueprint
from controllers.VenueController import *

venue = Blueprint('venue', __name__)

venue.route('/')(venues)
venue.route('/search', methods=['POST'])(search_venues)
venue.route('/<int:venue_id>')(show_venue)
venue.route('/create', methods=['GET'])(create_venue_form)
venue.route('/create', methods=['POST'])(create_venue_submission)
venue.route('/<venue_id>', methods=['DELETE'])(delete_venue)
venue.route('/<int:venue_id>/edit', methods=['GET'])(edit_venue)
venue.route('/<int:venue_id>/edit', methods=['POST'])(edit_venue_submission)
