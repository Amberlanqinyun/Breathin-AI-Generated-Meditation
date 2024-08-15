# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import session, redirect, url_for, render_template, app
from mod_db_account import searchCustomerById,searchStaffById

# Route to view profiles for customers and staff
@app.route('/view_profile', methods=['GET'])
def view_profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
   # Get the user's ID from the session
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    # Assign default values to prevent error when the particular role_id not in session
    staff_details = None
    customer_details = None
    # Determine which table to query based on the user's role
    if role_id in [2, 3]:  # Staff
        staff_details = searchStaffById(user_id)
    elif role_id in [1]:  # Customer
        customer_details = searchCustomerById(user_id)

    # Render the profile template with user details
    return render_template('view_profile.html', staff_details=staff_details, customer_details=customer_details)


@app.route('/view_staff_profile/<int:staff_id>', methods=['GET', 'POST'])
def view_staff_profile(staff_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
   
    # Assign default values to prevent error when the particular role_id not in session
    staff_details = None
    customer_details = None
    # Determine which table to query based on the user's role
    
    staff_details = searchStaffById(staff_id)
    isAdmin = 1

    # Render the profile template with user details
    return render_template('view_profile.html', staff_details=staff_details, customer_details=customer_details, isAdmin = isAdmin)


@app.route('/view_customer_profile/<int:customer_id>', methods=['GET', 'POST'])
def view_customer_profile(customer_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users
  
    # Assign default values to prevent error when the particular role_id not in session
    staff_details = None
    customer_details = None
    # Determine which table to query based on the user's role
    
    customer_details = searchCustomerById(customer_id)

    #check if it admin or stuff
    isAdmin = 1
    # Render the profile template with user details
    return render_template('view_profile.html', staff_details=staff_details, customer_details=customer_details, isAdmin=isAdmin)