# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
from mod_db_account import verify_reset_token, update_user_password
import bcrypt  # Import bcrypt for password hashing

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Check if the passwords match
        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('reset_password', token=token))
        
        # Verify the token to ensure it's valid and not expired
        user = verify_reset_token(token)
        
        if not user:
            flash('Invalid or expired token.')
            return redirect(url_for('login'))
        
        # Hash the new password using bcrypt
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update the password in the database
        update_user_password(user['UserID'], hashed_password)
        
        flash('Your password has been updated successfully.')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)
