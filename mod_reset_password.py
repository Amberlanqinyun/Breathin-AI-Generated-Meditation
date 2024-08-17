

# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import verify_reset_token, update_admin_password, update_user_password

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('reset_password', token=token))
        
        # Verify the token
        user = verify_reset_token(token)
        
        if not user:
            flash('Invalid or expired token.')
            return redirect(url_for('login'))
        
        # Update the password
        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        update_user_password(user['UserID'], hashed_password)
        
        flash('Your password has been updated successfully.')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)
