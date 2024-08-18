# Import necessary modules and functions
from mod_utilize import redirect, url_for, request, render_template, app, flash, session
from mod_db_account import listAllUsers

@app.route('/users', methods=['GET', 'POST'])
def view_users():
    # Check if the user is logged in and has admin access
    if 'user_id' not in session or session.get('role_id') != 1:
        flash("You don't have the necessary permissions to view this page.")
        return redirect(url_for('login'))
    role_id = session.get('role_id')
    
    # Handle search functionality
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')  # Get search query from form
        if search_query != '':
            search_query = '%' + search_query + '%'
            query = "WHERE UserID LIKE '{}' OR FirstName LIKE '{}' OR LastName LIKE '{}' OR Email LIKE '{}'".format(
                search_query, search_query, search_query, search_query)
        else:
            query = ''
        users = listAllUsers(query)
    else:
        users = listAllUsers()

    return render_template('view_users.html', users=users, role_id=role_id)
