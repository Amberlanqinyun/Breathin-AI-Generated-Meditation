from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from flask_bcrypt import Bcrypt
from flask import Flask, session, redirect, url_for, request, render_template, flash, send_file
import pymysql
from db_credentials import *
from db_baseOperation import execute_query

# Create a Flask application instance
app = Flask(__name__)

# Secret key to sign session cookies
app.secret_key = 'our_secret_key'

## CONTEXT PROCESSORS TO MAKE FUNCTIONS AND VARIABLES DIRECTLY AVAILABLE IN TEMPLATES ##

# Make the user details available on all templates after login so they don't need to be rendered.
@app.context_processor
def current_user_info():
    # Get the user's ID from the session
    user_id = session.get('user_id')
    # Get the role ID from the session
    role_id = session.get('role_id')

    # Check if a user is logged in
    if user_id and role_id:
        # Query the Users table to get user details
        query = "SELECT * FROM Users WHERE UserID = %s"
        
        # Execute the query to fetch user details
        user = execute_query(query, (user_id,), fetchone=True)
        
        # If user details are found
        if user:
            # Check if the user is an Admin or Regular User
            if role_id == 1:  # Admin
                user['role'] = 'Admin'
            elif role_id == 2:  # Regular User
                user['role'] = 'User'
            
            # Return a dictionary with the user details, including their role
            return {'current_user': user}
    
    # Return an empty dictionary if user is not logged in or not found
    return {}


# Create various variables used in multiple routes and templates
current_date = datetime.now().date()
tomorrow = current_date + relativedelta(days=1)
eighteen_years_ago = current_date - relativedelta(years=18)
# The number of days before subscription expires for displaying a heads-up to users and admins about membership expiry
days_before_expiry = 14
# String to insert in place of email for deactivated members
deactivated_email_string = "DEACTIVATED"

# Function to make re-used variables available for templates without needing to pass them via render_template each time.
@app.context_processor
def template_variables():
    # Insert the above variables into a dictionary for direct use in templates
    variables = {
        'current_date': current_date,
        'tomorrow': tomorrow,
        'eighteen_years_ago': eighteen_years_ago,
        'days_before_expiry': days_before_expiry,
        'deactivated_email_string': deactivated_email_string,
    }
    return variables

## TEMPLATE FILTERS TO ALLOW FOR CUSTOM FORMATTING IN TEMPLATES ##

# Define date formatting function and make it available for templates without needing to render it.
@app.template_filter('custom_date_format')
def custom_date_format(date_obj):
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
    elif isinstance(date_obj, date):
        date_obj = datetime(date_obj.year, date_obj.month, date_obj.day)
    return date_obj.strftime('%e %b %Y')

# Function for formatting times properly and made directly available in the templates
@app.template_filter('custom_time_format')
def custom_time_format(td):
    total_seconds = td.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    # Determine AM or PM
    am_pm = "AM" if hours < 12 else "PM"
    # Convert to 12-hour format
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12
    # Ensure time is formatted normally, so like 3:30 PM instead 03:30 PM or 14:30 PM
    formatted_time = "{:2d}:{:02d}".format(int(hours), int(minutes))
    # Add the AM or PM
    formatted_time = formatted_time + " " + am_pm