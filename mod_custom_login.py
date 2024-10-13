from mod_utilize import app, session, redirect, url_for, request, flash, render_template
from mod_db_account import authenticate_user
from mod_db_notifications import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        # Check if the user is an admin and redirect accordingly
        if session['role_id'] == 1:
            return redirect(url_for('admin_users'))
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
        print(f'Authenticated user: {user}')
        if user:
            # Authentication successful
            session['user_id'] = user['UserID']
            session['role_id'] = user['RoleID']
            flash('Login successful!', 'success')
            
            # Debugging: Print session variables
            print(f"User ID: {session['user_id']}, Role ID: {session['role_id']}")
            
            # Redirect based on role
            if session['role_id'] == 1:
                print("Redirecting to admin dashboard")
                return redirect(url_for('admin_users'))
            else:
                print("Redirecting to user dashboard")
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
