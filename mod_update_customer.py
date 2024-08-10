# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import   app, session, redirect, url_for, request, render_template, flash
import hashlib
from mod_db_account import searchCustomerById, searchCustomer, update_customer_details, update_customer_password

# Function to update customer profile
@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    # Ensure correct permissions
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # If invalid access role, redirect to dashboard
    role_id = session.get('role_id')
    # Get details to prefill the form
    customer_details = searchCustomerById(customer_id)
    # Get details from the form for updating table
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        existing_password = request.form['existing_password']
        # Check if staff email already exists, but is not the current staff's email
        customerInfo = searchCustomer(email)

        # If email is taken, prevent submission and display message
        if customerInfo != None and customerInfo["customer_id"] != customer_id:
            flash('Email taken, sorry. Please log in or use a different email.')
        else:

            if existing_password == '':
                update_customer_details(first_name,last_name,phone_number,email,address,customer_id)
                flash(first_name +"'s profile updated successfully")
                if role_id == customerInfo["role_id"]:
                    return redirect(url_for('view_profile'))
                else:
                    return redirect(url_for('view_customers'))
            else:
                new_password = request.form['new_password']
                new_password_confirm = request.form['new_password_confirm']
                # Check that new passwords are the same
                if new_password != new_password_confirm:
                    flash(
                        "Mismatch password with new password and comfirm new password.")
                else:
                    # Verify the existing password
                    pwd = hashlib.md5(existing_password.encode()).hexdigest()
                    # If existing password is entered and matches, proceed to next check
                    if customerInfo['password'] == pwd:
                        new_pwd = hashlib.md5(new_password.encode()).hexdigest()
                        update_customer_password(customer_id, new_pwd)
                        update_customer_details(
                            first_name, last_name, phone_number, email, address, customer_id)
                        # Inform them they updated the password
                        flash('Profile updated successfully, including password.')
                        if role_id == customerInfo["role_id"]:
                            return redirect(url_for('view_profile'))
                        else:
                            return redirect(url_for('view_customers'))
                        # Otherwise leave existing password blank and it remembers it
                    else:
                        flash( 'Invalid current password. Please provide the correct password')                  
    return render_template('update_customer.html', customer_details=customer_details, role_id= role_id)
