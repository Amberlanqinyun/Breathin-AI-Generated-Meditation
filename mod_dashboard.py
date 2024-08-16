# GROUP 2 PROJECT 2

# Import various modules created for and used in this python script
from mod_utilize import current_date, app, flash, session, redirect, url_for, render_template
from db_baseOperation import execute_query
from mod_db_orders import getFinishedOrderNumber,getOngoingOrderNumber,getOrderNumberByCustomerId
from mod_db_user_queries import getQueryNumber,getQueryNumberByCustomerId
from mod_db_notification import getUnreadNotificationCount, getNotificationCount
# Define a route for displaying the dashboard
@app.route('/dashboard')
def dashboard():
    # Get the user's ID from the session
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    # Set default message value to prevent error if not admin
    messages = ""
    
    # Check if the user is not logged in
    if user_id is None:
        # Display a flash message indicating the need to log in
        flash('Please log in to access the dashboard.')
        # Redirect the user to the login page if not logged in
        return redirect(url_for('login'))
    # Query the database for user details based on the user_id
    query = "SELECT * FROM customers WHERE customer_id = %s"
    user_details = execute_query(query, (user_id,), fetchone=True)
    # If user is not found in the members table, try querying the staff table
    if not user_details:
        query = "SELECT * FROM staff WHERE staff_id = %s"
        user_details = execute_query(query, (user_id,), fetchone=True)
    # If user is still not found, display an error message and redirect to login page
    if user_details is None:
        flash('User not found.')
        return redirect(url_for('login'))
    CustomerNumber = 0
    QueriesNumber=0
    if role_id == 1:
        CustomerNumber = getQueryNumberByCustomerId(user_id)['count']
    else:
        QueriesNumber=getQueryNumber()['count']
    # Display the dashboard template
    customerOrderNumber = getOrderNumberByCustomerId(user_id)['count']
    
    FinishedOrderNumber =getFinishedOrderNumber()['count']
    notificationNumber = 0
    if role_id == 1:
        count = getUnreadNotificationCount(user_id)
        if count:
            notificationNumber = count['count']
    else:
        notificationNumber = getNotificationCount()['count']
    ActiveOrderNumber = getOngoingOrderNumber()['count']
    return render_template('dashboard.html', user_details=user_details, messages=messages, customerOrderNumber = customerOrderNumber,
                           CustomerNumber= CustomerNumber,QueriesNumber= QueriesNumber,FinishedOrderNumber= FinishedOrderNumber, ActiveOrderNumber= ActiveOrderNumber,notificationNumber = notificationNumber)
