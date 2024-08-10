# GROUP 2 PROJECT 2

# Import various modules created for and used in this python srcipt
from mod_utilize import session, redirect, url_for, request, render_template, flash, app
import hashlib
from mod_db_account import searchStaff, searchStaffById, searchCustomer, update_staff_details,update_password

# Function to update staff profile
@app.route('/update_staff/<int:staff_id>', methods=['GET', 'POST'])
def update_staff(staff_id):
    # Confirm user is logged in before granting access to this page
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # If invalid access role redirect to dashboard
    role_id = session.get('role_id')
    if role_id not in [2, 3]:
        return redirect(url_for('dashboard'))
    # Get details to prefill the form
    staff_details = searchStaffById(staff_id)
    
    # Get details from the form for updating table
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        existing_password = request.form['existing_password']
        # Check if staff email already exists, but is not the current staff's email
        staffInfo =  searchStaff(email)
        
        # If email is taken, prevent submission and display message
        if staffInfo != None and staffInfo["staff_id"] != staff_id:
            flash('Email taken, sorry. Please log in or use a different email.')
        else :
                 
            if existing_password == '':
                update_staff_details(first_name, last_name, phone_number, email, staff_id)
                flash('Profile updated successfully')
            else:
                new_password = request.form['new_password']
                new_password_confirm = request.form['new_password_confirm']
                # Check that new passwords are the same
                if new_password != new_password_confirm:
                    flash("Mismatch password with new password and comfirm new password.")
                else:
                    # Verify the existing password
                    pwd = hashlib.md5(existing_password.encode()).hexdigest()
                        # If existing password is entered and matches, proceed to next check
                    if staffInfo['password'] == pwd:
                        new_pwd = hashlib.md5(new_password.encode()).hexdigest()
                        update_password(staff_id, new_pwd)
                        update_staff_details(first_name, last_name, phone_number, email, staff_id)
                            # Inform them they updated the password
                        flash('Profile updated successfully, including password.')
                        # Otherwise leave existing password blank and it remembers it
                    else:
                        flash('Invalid current password. Please provide the correct password')
    staff_details = searchStaffById(staff_id)
    return render_template('update_profile.html', staff_details=staff_details, role_id = role_id)

    