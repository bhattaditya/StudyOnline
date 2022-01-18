Interactive Web Application (flask)
>User first have to login if not registered.

What can a user do?
- Related to basic details
    User can modify username, email if not taken by already by another user also user can update profile picture.(user account)

- Related to Rooms, user can
    1. Create Room
    2. Modify Room
    3. Delete Room

User can view another user profile, rooms, topics and partcipants.

Only LoggedIn user have the visibility to edit or delete rooms.


What else can be done?
 password reset mechanism


Blueprint is a way to organize flask application into smaller and re-usable application (packages).
    forms.py
    routes.py

config file contains all the configuration related to application.

Creating app as function will be very helpful as we can change the configurations and create testing environments.

create_app() function will remove all app keywords and we just need to import current_app from flask module to use app.

Flask Migration  - helps to edit database without creating from start




Next project - Student Management System.