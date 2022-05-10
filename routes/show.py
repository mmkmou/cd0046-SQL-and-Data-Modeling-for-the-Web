from flask import Blueprint
from controllers.ShowController import shows, create_shows, create_show_submission

show = Blueprint('show', __name__)


show.route('/')(shows)
show.route('/create')(create_shows)
show.route('/create', methods=['POST'])(create_show_submission)
