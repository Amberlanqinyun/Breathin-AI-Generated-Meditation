# GROUP 2 PROJECT 2

# Import necessary modules and functions
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
from mod_db_account import insertStaff, searchStaff, hash_password,searchCustomer,insertCustomer
from datetime import date


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    role_id = session.get('role_id')
    if 'user_id' not in session or role_id != 3:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        role_id = request.form['role_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']


        if searchStaff(email):
            flash('Email taken, sorry. Please log in or use a different email.')
            return render_template('create_account.html', role_id=role_id, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)

        
        hashed_password = hash_password('1')  # Set the default password to '1'

        employment_start_date = date.today()  # Get today's date
        
        # Utilizing the insertStaff function from db_baseOperation
        insertStaff(role_id, first_name, last_name, phone_number, email, hashed_password, employment_start_date)
        flash('Account created successfully.')
        
    return render_template('create_account.html')



@app.route('/create_customer_account', methods=['GET', 'POST'])
def create_customer_account():
    role_id = session.get('role_id')
    if 'user_id' not in session or role_id == 1:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        dob = request.form['date_of_birth']
        address = request.form['address']


        if searchCustomer(email):
            flash('Email taken, sorry. Please use a different email.')
            return render_template('create_customer_account.html')

        
        hashed_password = hash_password('123456')  # Set the default password to '1'
        
        # Utilizing the insertStaff function from db_baseOperation
        insertCustomer(first_name, last_name, phone_number, email, hashed_password, address, dob)
        flash('Account created successfully.')
        
    return render_template('create_customer_account.html')
    