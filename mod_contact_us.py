# GROUP 2 PROJECT 2

# Import necessary modules and functions
from mod_utilize import flash, render_template, request, app,session
from mod_db_customer_queries import addANewQueries
from mod_db_account import searchCustomerById

# Route to update news for all members and staff
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    customerDetails = None
    if request.method == 'POST':
        # Get the contact_us info from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        message = request.form['message']

        # Insert message into the contact_us table for admins to see
        addANewQueries(first_name,last_name,phone_number,email,message)
        # Display success message
        flash('Message successfully sent. We will be in touch as soon as we are able')

    
    if 'user_id' in session:
        user_id = session['user_id']
        customerDetails = searchCustomerById(user_id)

    return render_template('contact_us.html', customerDetails = customerDetails)
