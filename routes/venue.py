from flask import Blueprint
from controllers.VenueController import delete_venue, venues, search_venues, show_venue, create_venue_form, create_venue_submission, delete_venue, edit_venue, edit_venue_submission

venue = Blueprint('venue', __name__)

venue.route('/')(venues)
venue.route('/search', methods=['POST'])(search_venues)
venue.route('/<int:venue_id>')(show_venue)
venue.route('/create', methods=['GET'])(create_venue_form)
venue.route('/create', methods=['POST'])(create_venue_submission)
venue.route('/<int:venue_id>/delete', methods=['GET'])(delete_venue)
venue.route('/<int:venue_id>/edit', methods=['GET'])(edit_venue)
venue.route('/<int:venue_id>/edit', methods=['POST'])(edit_venue_submission)
