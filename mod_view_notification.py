# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import redirect, url_for, request, render_template, app, flash, session
from mod_db_notifications import *


@app.route('/view_notification', methods=['GET','POST'])
def view_notification():
    # Check if the user is logged in and has admin access
    if 'user_id' not in session :
        flash("You don't have the necessary permissions to view this page.")
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    count = 0
    query = ""
    if request.method == 'POST':
        search_query = request.form.get(
            'search_query', '')  # Get search query from form
        if search_query == '':
            query = ""
        else:
        # Wildcard symbols for partial matching
            search_query = '%' + search_query + '%'
        # Query the customers table to get a list of matching customers by ID, first name, or last name
            query = "  ( notification.notification_id LIKE '{}' OR customers.first_name LIKE '{}' OR notification.notification_time LIKE '{}' OR notification.details LIKE '{}')".format(
                search_query, search_query, search_query, search_query)
        
    # Handle search functionality
    if role_id == 1:
        notifications = searchNotificationById(user_id,query)
        count = getUnreadNotificationCount(user_id)
    else:
        notifications = searchNotification(query)
        count = getNotificationCount()

    for notification in notifications:
        notification['notification_time'] = notification['notification_time'].strftime('%e %b %Y %H:%M:%S')

    return render_template('view_notification.html', notifications=notifications, count=count)
