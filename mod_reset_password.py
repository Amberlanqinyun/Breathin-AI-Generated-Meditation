import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template, request, redirect, url_for, flash
from mod_utilize import app
from mod_db_user_management import get_user_by_email, update_user_password, verify_reset_token, generate_reset_token, searchUser
from mod_db_account import send_reset_email, generate_random_password,hash_password


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('reset_password', token=token))
        
        user = verify_reset_token(token)
        
        if not user:
            flash('Invalid or expired token.')
            return redirect(url_for('login'))
        
        hashed_password = hash_password(new_password)
        update_user_password(user['UserID'], hashed_password)
        
        flash('Your password has been updated successfully.')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)