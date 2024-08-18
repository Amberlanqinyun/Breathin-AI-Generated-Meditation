# Import necessary modules and functions
from mod_utilize import flash, render_template, request, app, session, redirect, url_for
from mod_db_user_queries import addANewQueries
from mod_db_account import searchUserById

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    userDetails = None
    
    if request.method == 'POST':
        # Get the feedback info from the form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Server-side validation (if required)
        if not first_name or not last_name or not email or not message:
            flash('All fields are required. Please fill out the form completely.', 'danger')
            return render_template('contact_us.html', userDetails=userDetails)
        
        # Insert the message into the feedback/queries table for admins to review
        addANewQueries(first_name, last_name, email, message)
        
        # Display success message and redirect to a confirmation or home page
        flash('Message successfully sent. We will be in touch as soon as we are able.', 'success')
        return redirect(url_for('contact_us'))  # Redirect to the same page to show the flash message
    
    # If the user is logged in, retrieve their details
    if 'user_id' in session:
        user_id = session['user_id']
        userDetails = searchUserById(user_id)

    # Render the feedback page
    return render_template('contact_us.html', userDetails=userDetails)
