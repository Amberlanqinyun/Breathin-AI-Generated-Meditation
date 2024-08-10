# GROUP 2 PROJECT 2

# Import various modules created for and used in this python script
from mod_utilize import  app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import searchCustomer, searchStaff
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
        # Check if user exists in staff table and verify password
        
        user = searchStaff(email)
        count = 0
        if user:
            # If user is found and password is correct, log in
            pwd = hashlib.md5(password.encode()).hexdigest()
            notification_count = getNotificationCount()
            
            if notification_count['count']:
                count  = notification_count['count']
            if user and user['password'] == pwd:
         # Store user's ID and role_id in the session
                session['user_id'] = user['staff_id'] if 'staff_id' in user else user['customer_id']
                session['role_id'] = user['role_id']
                session['notification_number'] = count
            # If the staff is logging in for the first time, redirect to change password page
                if pwd == hashlib.md5('1'.encode()).hexdigest():
                    session['change_password'] = True
                    return redirect(url_for('change_password'))
                return redirect(url_for('dashboard'))
            else:
                # If login fails, show an error message and redirect back to login page
                flash('Invalid email or password. Please try again.')
                return redirect(url_for('login'))
        # If user is not found in staff table, check in members table
        else:
            user = searchCustomer(email)
            # If user is found and password is correct, log in
            pwd = hashlib.md5(password.encode()).hexdigest()
            
           
            if user and user['password'] == pwd and user['banned'] == 0:
             # Store user's ID and role_id in the session
                notification_count = getUnreadNotificationCount(user['customer_id'])
                # Check for overdue notifications
                send_overdue_notifications()
                if notification_count:
                    count = notification_count['count']
                session['user_id'] = user['customer_id'] 
                session['role_id'] = user['role_id']
                session['notification_number'] = count
        
                if pwd == hashlib.md5('123456'.encode()).hexdigest():
                    session['change_password'] = True
                    return redirect(url_for('change_password'))
                else:
                    return redirect(url_for('dashboard')) 
            else:
                # If login fails, show an error message and redirect back to login page
                flash('Invalid email or password. Please try again.')
                return redirect(url_for('login'))
            # Display the login form
    return render_template('login.html')


# Function to log out
@app.route('/logout')
def logout():
    # Clear the user_id from the session to log out the user
    session.pop('user_id', None)
    # Display homepage page
    return redirect(url_for('index'))

