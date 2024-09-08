# Import necessary modules created for and used in this Python script
from mod_utilize import session, redirect, url_for, render_template, app
from mod_db_account import searchUserById

# Route to view profiles for users and admins
@app.route('/view_profile', methods=['GET'])
def view_profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
    
    # Get the user's ID from the session
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    
    # Assign default values to prevent errors when the particular role_id is not in session
    user_details = None

    user_details = searchUserById(user_id)

    # Render the profile template with user details
    return render_template('view_profile.html', user_details=user_details)


# Route to view specific user profile
@app.route('/view_user_profile/<int:user_id>', methods=['GET', 'POST'])
def view_user_profile(user_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
  
    # Assign default values to prevent error when the particular role_id not in session
    user_details = searchUserById(user_id)

    # Check if it is admin or user
    isAdmin = 1
    # Render the profile template with user details
    return render_template('view_profile.html', admin_details=None, user_details=user_details, isAdmin=isAdmin)
