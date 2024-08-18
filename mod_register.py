# Import necessary modules and functions
from mod_utilize import app, flash, session, redirect, url_for, render_template, request
import hashlib
from mod_db_account import searchUser, insertUser

# Define the route for user registration with HTTP methods GET and POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Ensure no one is logged in
    if 'user_id' in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['new_password']
        confirm_password = request.form['new_password_confirm']

        # Check password strength
        if len(password) < 6 or not any(character.isdigit() for character in password) or not any(character.isalpha() for character in password):
            flash('INVALID password. Must be at least 6 characters and include both letters and numbers.')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Mismatched password and confirm password.')
            return render_template('register.html')
        
        # Check if the email exists in the Users table
        existing_email = searchUser(email)
        if existing_email:
            flash('Email is already taken. Please use a different email.')
            return render_template('register.html')
        else:
            # Insert user data into the Users table
            result = insertUser(first_name, last_name, email,password)
            
            # Check if the user was successfully inserted
            if result:
                flash('Registration successful! You may now log in.')
                return redirect(url_for('login'))
            else:
                flash('Account creation failed. Please contact support for help.')
                return render_template('register.html')
    
    # Render the registration form template if method is GET or registration fails
    return render_template('register.html')
