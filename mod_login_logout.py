from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import *
from mod_db_notification import *

def hash_password(password):
    """Returns the MD5 hash of the given password."""
    return hashlib.md5(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate the user by checking both Admin and User tables."""
    pwd_hash = hash_password(password)
    
    # Check if user exists in Admin table
    user = searchAdmin(email)
    if user and user['PasswordHash'] == pwd_hash:
        return user, True  # Admin user

    # Check if user exists in User table
    user = searchUser(email)
    if user and user['PasswordHash'] == pwd_hash and not user['banned']:
        return user, False  # Regular user
    
    return None, None  # User not found or password incorrect

### LOG IN/OUT FUNCTIONS ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        if email:
            session['email'] = email
            return redirect(url_for('enter_password'))  # Ensure this matches the actual route name
        else:
            flash('Please enter a valid email address', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/enter_password', methods=['GET', 'POST'])
def enter_password():
    email = session.get('email')
    if not email:
        flash('Please enter your email first.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        user, is_admin = authenticate_user(email, password)
        
        if user:
            if is_admin:
                notification_count = getNotificationCount()
            else:
                notification_count = getUnreadNotificationCount(user['UserID'])
            
            count = notification_count['count'] if notification_count and notification_count['count'] else 0

            session['user_id'] = user['AdminID'] if is_admin else user['UserID']
            session['role_id'] = user['RoleID']
            session['notification_number'] = count

            if password in ['1', '123456']:
                session['change_password'] = True
                return redirect(url_for('change_password'))

            return redirect(url_for('dashboard'))
        
        flash('Invalid password. Please try again.')
        return redirect(url_for('enter_password'))

    return render_template('password.html', email=email)

@app.route('/logout')
def logout():
    session.clear()  # Clears the entire session, not just specific keys
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

