# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import redirect, url_for, request, render_template, app, flash,session
from mod_db_account import listAllCustomers

@app.route('/customers', methods=['GET', 'POST'])
def view_customers():
    # Check if the user is logged in and has admin access
    if 'user_id' not in session or session.get('role_id') == 1:
        flash("You don't have the necessary permissions to view this page.")
        return redirect(url_for('login'))
    role_id = session.get('role_id')
    # Handle search functionality
    if request.method == 'POST':
        search_query = request.form.get(
            'search_query', '')  # Get search query from form
        if search_query != '':
        # Wildcard symbols for partial matching
            search_query = '%' + search_query + '%'
        # Query the customers table to get a list of matching customers by ID, first name, or last name
            query = "WHERE customer_id LIKE '{}' OR first_name LIKE '{}' OR last_name LIKE '{}' OR phone_number LIKE '{}' OR email LIKE '{}' OR date_of_birth LIKE '{}'".format(
                search_query, search_query, search_query, search_query, search_query, search_query)
        else:
            query = ''
        customers = listAllCustomers(query)
    else:
        customers = listAllCustomers()

    return render_template('view_customers.html', customers=customers,role_id = role_id)
