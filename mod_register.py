# Import necessary modules and functions
from mod_utilize import app, flash, session, redirect, url_for, render_template, request
from mod_db_account import searchUser, insertUser, hash_password

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['new_password']
        confirm_password = request.form['new_password_confirm']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        # Check if email already exists
        if searchUser(email):
            flash('Email is already registered. Please log in or use another email.', 'danger')
            return render_template('register.html')

        # Insert the new user into the database (password is passed as raw string)
        if insertUser(first_name, last_name, email, password):
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error during registration. Please try again.', 'danger')
    
    return render_template('register.html')
