# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import search_user, generate_reset_token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from mod_db_account import send_reset_email


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        print(f"Received email: {email}")  # Debugging statement
        
        user = search_user(email)
        print(f"User found: {user}")  # Debugging statement
        
        if user:
            token = generate_reset_token(user['UserID'])
            print(f"Generated token: {token}")  # Debugging statement
            
            send_reset_email(email, token)
            print(f"Reset email sent to: {email}")  # Debugging statement
            
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('No account found with that email.', 'danger')
    
    return render_template('forgot_password.html')

