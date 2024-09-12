from mod_utilize import app, session, redirect, url_for, request, flash, render_template
from mod_db_account import *
from mod_db_notifications import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        if email:
            session['email'] = email
            return redirect(url_for('enter_password'))
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
        user = authenticate_user(email, password)  # Correctly handle the user authentication
        
        if user:
            # Authentication successful
            notification_count = getUnreadNotificationCount(user['UserID'])  # User-specific notifications
            count = notification_count['count'] if notification_count and notification_count['count'] else 0
            
            session['user_id'] = user['UserID']
            session['role_id'] = user['RoleID']
            session['notification_number'] = count
            
            # Redirect user to dashboard
            return redirect(url_for('dashboard'))
        
        # Authentication failed
        flash('Invalid email or password. Please try again.', 'danger')
        return redirect(url_for('enter_password'))

    return render_template('password.html', email=email)


@app.route('/logout')
def logout():
    session.clear()  # Clears the entire session
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
