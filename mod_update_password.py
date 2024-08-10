# GROUP 2 PROJECT 2

# Import various modules created for and used in this python script
from mod_utilize import  app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import update_password,update_customer_password



@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'change_password' not in session or not session['change_password']:
        flash('Access denied.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_id = session['user_id']
        role_id = session['role_id']
        if new_password == confirm_password:
            if role_id == 1:
                update_customer_password(session['user_id'], hashlib.md5(new_password.encode()).hexdigest())
            else:
                update_password(session['user_id'], hashlib.md5(new_password.encode()).hexdigest())
            flash('Password updated successfully.')
            session.pop('change_password', None)  # Remove the change_password flag from the session
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.')
    
    return render_template('change_password.html')