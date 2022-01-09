"""
Flask-Login provides user session management. 
It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods of time.
"""

import secrets
from os import path
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from studyonline import app, db, bcrypt
from studyonline.models import User, Room
from studyonline.forms import LoginForm, RegistrationForm, UpdateAccountForm, CreateRoomForm, UpdateRoomForm

@app.route('/')
def home():
    """
    Home Page/ Landing Page
    """
    rooms = Room.query.order_by(Room.date_created.desc()).all()
    return render_template('home.html', title='Home', rooms=rooms)

@app.route('/about')
def about():
    """
    About the site
    """

    return render_template('about.html', title='About')

@app.route('/room/<int:pk>')
@login_required
def room(pk):
    """
    Different rooms created by users.
    """
    rooms = Room.query.all()

    found_room = None
    for room in rooms:
        if room.id == pk:
            found_room = room

    return render_template('room.html',title='Room', room=found_room)

@app.route('/login', methods=['GET','POST'])
def login():
    """
    This will make the user logIn to system.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Incorrect username and password!', 'danger')
    return render_template('login.html', title='Login',form=form)

@app.route('/logout')
def logout():
    """
    This will terminate current user session.
    """

    logout_user()
    flash('Logged out! see you next time.', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET','POST'])
def register():
    """
    flask_login module provides various variables and classes.
    
    Variable:
        current_user: user that is currently logged in and its properties can be accessed.

    Functions:
        url_for()
        redirect()
        flash()
        render_template()

    Class Objects:
        form - RegistrationForm class
        user - User class
    """

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def save_picture(form_picture):
    """
    This will reduce the resolution a file and then save it to a specific loaction i.e 'static/profile_pics'.

    random_hex : will generate a number alpha numeric numbers
    file_ext: with help of os module, file is split to generate --> tuple(filename, extension) 
    picture: genreated filename -> random_hex.file_ext
    picture_path: path is created so that picutre can be saved to static/profile_pics sub directory
    """

    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(form_picture.filename)
    picture = random_hex + file_ext
    picture_path = path.join(app.root_path, 'static/profile_pics', picture)
    output_size = (120, 120)
    pic = Image.open(form_picture)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    """
    Logged In user can update the details like username, email if not already taken.
    User can also upload profile pic.
    """

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.image_file = picture

        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated!', 'success')
        return redirect(url_for('account'))
    if request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title="Account", form=form)

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    """
    This will create a new room.
    """
    form= CreateRoomForm()
    if form.validate_on_submit():
        room = Room(topic=form.topic.data, description=form.description.data, user_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        flash('Room Created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_room.html', form=form)

@app.route('/profile/<string:username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', title='Profile', user=user)

@app.route('/update_room/<int:pk>', methods=['GET', 'POST'])
@login_required
def update_room(pk):
    """
    This will update a existing room.
    """
    room = Room.query.get_or_404(pk)
    form = UpdateRoomForm()
    if form.validate_on_submit():
        room.topic = form.topic.data
        room.description = form.description.data
        db.session.commit()
        flash('Room Updated!', 'success')
        return redirect(url_for('home'))

    elif request.method == 'GET':
        # room = Room(topic=form.topic.data, description=form.description.data, user_id=current_user.id)
        form.topic.data = room.topic
        form.description.data = room.description

    return render_template('update_room.html', title='Update',form=form) 

@app.route('/delete_room/<int:pk>', methods=['GET', 'POST'])
def delete_room(pk):
    """
    This will delete an existing room.
    """
    room = Room.query.get_or_404(pk)
    db.session.delete(room)
    db.session.commit()
    flash('Room Deleted!', 'success')
    return redirect(url_for('home'))