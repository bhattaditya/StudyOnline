import time
from flask import Blueprint, url_for, redirect, render_template, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from studyonline.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from studyonline.users.utils import save_picture
from studyonline.models import User, Room
from studyonline import db, bcrypt


users = Blueprint('users', __name__)

@users.route('/login', methods=['GET','POST'])
def login():
    """
    This will make the user logIn to system.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
        else:
            flash('Incorrect username and password!', 'danger')
    return render_template('login.html', title='Login',form=form)

@users.route('/logout')
def logout():
    """
    This will terminate current user session.
    """

    logout_user()
    time.sleep(2)
    flash('Logged out! see you next time.', 'success')
    return redirect(url_for('main.home'))

@users.route('/register', methods=['GET','POST'])
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
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        time.sleep(1)
        flash('Successfully registered!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/account', methods=['GET','POST'])
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
        time.sleep(1)
        flash('Account Updated!', 'success')
        return redirect(url_for('users.account'))
    if request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title="Account", form=form)

@users.route('/profile/<string:username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', title='Profile', user=user)

@users.route('/user_rooms/<string:username>')
def user_rooms(username):
    """
    Displays all rooms of a user
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    rooms = Room.query.filter_by(creator=user)\
                .order_by(Room.date_created.desc())\
                    .paginate(per_page=5, page=page)
    
    return render_template('user_rooms.html', title='Rooms',rooms=rooms, user=user) 