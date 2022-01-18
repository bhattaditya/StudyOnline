from flask import Blueprint, request, render_template
from studyonline.models import Room

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """
    Home Page/ Landing Page
    """
    
    page = request.args.get('page', 1, type=int)
    rooms = Room.query.order_by(Room.date_created.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', title='Home', rooms=rooms)

@main.route('/about')
def about():
    """
    About the site
    """

    return render_template('about.html', title='About')