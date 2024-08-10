# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import session, redirect, url_for, render_template, flash, app,request
from mod_db_account import listAllStaffs

# Route to view staffs to choose from for booking individual swimming lessons
@app.route('/view_staffs', methods=['GET','POST'])
def view_staffs():
    # Check if the user is logged in and if they have the role_id of 1
    # Redirect them to the login page if not authorized
    if 'user_id' not in session or session.get('role_id') == 1:
        flash("You don't have the necessary permissions to view this page.")
        return redirect(url_for('login'))
    
    staff = None
    if request.method == 'POST':
        search_query = request.form.get(
            'search_query', '')  # Get search query from form
        if search_query != '':
        # Wildcard symbols for partial matching
            search_query = '%' + search_query + '%'
        # Query the customers table to get a list of matching customers by ID, first name, or last name
            query = "WHERE staff_id LIKE '{}' OR first_name LIKE '{}' OR last_name LIKE '{}' OR phone_number LIKE '{}' OR email LIKE '{}' OR employment_start_date LIKE '{}'".format(
                search_query, search_query, search_query, search_query, search_query, search_query)
        else: 
            query = ''
        staffs = listAllStaffs(query)
    else:    # Query to retrieve all staffs
        staffs = listAllStaffs()
        # Render the view_staffs.html template with the fetched staffs data
    return render_template('view_staffs.html', staffs=staffs)
