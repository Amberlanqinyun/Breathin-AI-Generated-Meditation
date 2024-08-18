# Import necessary modules created for and used in this Python script
from mod_utilize import session, redirect, url_for, render_template, app
from mod_db_account import searchUserById, searchAdminById

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
    admin_details = None
    
    # Determine which table to query based on the user's role
    if role_id == 1:  # Admin
        admin_details = searchAdminById(user_id)
    elif role_id == 2:  # User
        user_details = searchUserById(user_id)

    # Render the profile template with user details
    return render_template('view_profile.html', admin_details=admin_details, user_details=user_details)

# Route to view specific admin profile
@app.route('/view_admin_profile/<int:admin_id>', methods=['GET', 'POST'])
def view_admin_profile(admin_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
   
    # Assign default values to prevent error when the particular role_id not in session
    admin_details = searchAdminById(admin_id)
    isAdmin = 1

    # Render the profile template with user details
    return render_template('view_profile.html', admin_details=admin_details, user_details=None, isAdmin=isAdmin)

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
