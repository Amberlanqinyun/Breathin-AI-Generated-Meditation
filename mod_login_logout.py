
# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import *
from mod_db_notification import *

### LOG IN/OUT FUNCTIONS ###
# Function for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    # If the request method is POST, process the login attempt
    if request.method == 'POST':
        # Get email and password from the login form
        email = request.form['email']
        password = request.form['password']
        pwd = hashlib.md5(password.encode()).hexdigest()  # Encrypt the password

        # Check if the user exists in the Admin table
        user = searchAdmin(email)
        if user:
            if user['PasswordHash'] == pwd:
                notification_count = getNotificationCount()
                count = notification_count['count'] if notification_count['count'] else 0

                # Store user's ID and role_id in the session
                session['user_id'] = user['AdminID']
                session['role_id'] = user['RoleID']
                session['notification_number'] = count

                # If the admin is logging in for the first time, redirect to change password page
                if pwd == hashlib.md5('1'.encode()).hexdigest():
                    session['change_password'] = True
                    return redirect(url_for('change_password'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again.')
                return redirect(url_for('login'))
        
        # If the user is not found in the Admin table, check in the User table
        else:
            user = searchUser(email)
            if user and user['PasswordHash'] == pwd and not user['banned']:
                notification_count = getUnreadNotificationCount(user['UserID'])
                send_overdue_notifications()  # Check for overdue notifications

                count = notification_count['count'] if notification_count else 0

                # Store user's ID and role_id in the session
                session['user_id'] = user['UserID']
                session['role_id'] = user['RoleID']
                session['notification_number'] = count

                # If the user is logging in for the first time, redirect to change password page
                if pwd == hashlib.md5('123456'.encode()).hexdigest():
                    session['change_password'] = True
                    return redirect(url_for('change_password'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again.')
                return redirect(url_for('login'))

    # Display the login form
    return render_template('login.html')

# Function to log out
@app.route('/logout')
def logout():
    # Clear the user_id from the session to log out the user
    session.pop('user_id', None)
    # Redirect to the homepage
    return redirect(url_for('index'))
