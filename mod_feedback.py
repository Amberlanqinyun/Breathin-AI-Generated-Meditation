# GROUP 2 PROJECT 2

# Import necessary modules and functions
from mod_utilize import flash, render_template, request, app, session
from mod_db_user_queries import addANewQueries
from mod_db_account import searchUserById

# Route to handle feedback submission and display user details
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    userDetails = None
    if request.method == 'POST':
        # Get the feedback info from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        message = request.form['message']

        # Insert message into the feedback or queries table for admins to see
        addANewQueries(first_name, last_name, email, message)
        # Display success message
        flash('Message successfully sent. We will be in touch as soon as we are able')

    # If the user is logged in, retrieve their details
    if 'user_id' in session:
        user_id = session['user_id']
        userDetails = searchUserById(user_id)

    return render_template('feedback.html', userDetails=userDetails)

