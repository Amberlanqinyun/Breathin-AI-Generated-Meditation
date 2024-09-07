from flask import render_template, request, redirect, url_for, flash, session, jsonify
from mod_utilize import app,datetime
from mod_db_account import get_user_profile,update_user_profile

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to edit your profile.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Fetch the form data and update the user's profile in the database
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        
        # Update the user profile in the database
        update_user_profile(user_id, first_name, last_name, email)
        flash("Profile updated successfully.", "success")
        return redirect(url_for('dashboard'))
    
    # Fetch current user profile data to populate the form
    user_profile = get_user_profile(user_id)
    
    return render_template('edit_profile.html', user_profile=user_profile)
