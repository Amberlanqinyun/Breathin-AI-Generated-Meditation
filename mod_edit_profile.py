from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from mod_utilize import app
from mod_db_account import get_user_profile, update_user_profile, update_user_password, hash_password

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to edit your profile.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Fetch the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate the passwords if they are provided
        if password and confirm_password:
            if password != confirm_password:
                flash("Passwords do not match. Please try again.", "error")
                return render_template('edit_profile.html', user_profile=get_user_profile(user_id))

            # If passwords match and are not placeholders, update the password
            if password and password != "******":
                # Hash the password before storing
                password_hash = hash_password(password)
                password_updated = update_user_password(user_id, password_hash)
                
                if password_updated:
                    flash("Password updated successfully.", "success")
                else:
                    flash("Error updating password.", "error")
        
        # Update user details
        try:
            update_user_profile(first_name, last_name, email, user_id)
            flash("Profile updated successfully.", "success")
        except Exception as e:
            flash(f"Error updating profile: {e}", "error")
        
    # Fetch current user profile data to populate the form
    user_profile = get_user_profile(user_id)
    
    return render_template('edit_profile.html', user_profile=user_profile)
