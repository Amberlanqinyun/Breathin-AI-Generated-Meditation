
# Import necessary modules and functions
from mod_utilize import  app, flash, session, redirect, url_for, render_template, request, datetime, relativedelta
# PythonAnywhere won't allow these ones to be imported like the above ones
import os
import hashlib
from PIL import Image
from db_account import searchCustomer, searchStaff,insertCustomer


# Define the route for user registration with HTTP methods GET and POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Ensure no one logged in
    if 'user_id' in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['new_password']
        confirmPassword = request.form['new_password_confirm']

        # # Check password strength
        if len(password) < 6 or not any(character.isdigit() for character in password) or not any(character.isalpha() for character in password):
            flash('INVALID password. Must be at least 6 characters and include both letters and numbers.')
            # Redirect back to registration
            return render_template('register.html')
        if password != confirmPassword:
            flash('Mismatched password and comfirmPassword. ')
            # Redirect back to registration
            return render_template('register.html')
        
        # Check if the email exists in either staff or customer tables
        existing_email = searchStaff(email)
        if existing_email:
            flash('Email taken, sorry. Please use a different email.')
            return render_template('register.html')

        else:
            existing_email = searchCustomer(email)
            if existing_email:
                flash('Email taken, sorry. Please use a different email.')
                return render_template('register.html')

            else:
                # encrypt the password using bcrypt
                pwd = hashlib.md5(password.encode()).hexdigest()
                # Insert customer data into the customers table
                result = insertCustomer(first_name,last_name,email,pwd)
                # Display success message and redirect
                result = searchCustomer(email)
                if result:
                    flash('registeration successful! You may now log in.')
                    return redirect(url_for('login'))
                else:
                    flash('Create account failed, please contact for help')
                    return render_template('register.html')
                
    # Render the registration form template if method is GET or registration fails
    return render_template('register.html', )