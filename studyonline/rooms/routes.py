import time
from flask import Blueprint, render_template, redirect, url_for, abort, flash, request
from studyonline import db
from flask_login import current_user, login_required
from studyonline.models import Room, User
from studyonline.rooms.forms import CreateRoomForm


rooms = Blueprint('rooms', __name__)

@rooms.route('/room/<int:pk>')
@login_required
def room(pk):
    """
    Different rooms created by users.
    """
    room = Room.query.get_or_404(pk)

    return render_template('room.html',title='Room', room=room)

@rooms.route('/create_room', methods=['GET', 'POST'])
def create_room():
    """
    This will create a new room.
    """
    form= CreateRoomForm()
    if form.validate_on_submit():
        room = Room(topic=form.topic.data, description=form.description.data, creator=current_user)
        db.session.add(room)
        db.session.commit()
        time.sleep(1)
        flash('Room Created!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('create_room.html', form=form)



@rooms.route('/update_room/<int:pk>', methods=['GET', 'POST'])
@login_required
def update_room(pk):
    """
    This will update a existing room.
    """
    room = Room.query.get_or_404(pk)
    if room.creator != current_user:
        abort(403)

    form = CreateRoomForm()
    if form.validate_on_submit():
        room.topic = form.topic.data
        room.description = form.description.data
        db.session.commit()
        flash('Room Updated!', 'success')
        return redirect(url_for('main.home'))

    elif request.method == 'GET':
        form.topic.data = room.topic
        form.description.data = room.description
        form.submit.label.text = "Update Room"
    return render_template('create_room.html', title='Update',form=form) 

@rooms.route('/delete_room/<int:pk>', methods=['GET','POST'])
@login_required
def delete_room(pk):
    """
    This will delete an existing room.
    """
    
    room = Room.query.get_or_404(pk)
    if room.creator != current_user:
        abort(403)
    
    db.session.delete(room)
    db.session.commit()
    time.sleep(1)
    flash('Room deleted!', 'success')
    return redirect(url_for('main.home'))

@rooms.route('/search_email',methods=['POST'])
def search_email():
    """
    Lists all rooms of a user if email provided.
    """
    email = request.form.get('input-email')

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=email).first()
    
    if user:
        rooms = Room.query.filter_by(creator=user)\
                .order_by(Room.date_created.desc())\
                    .paginate(per_page=5, page=page)
        return render_template('user_rooms.html', rooms=rooms, user=user)
    return render_template('common.html', message="No such email found.")

    
    