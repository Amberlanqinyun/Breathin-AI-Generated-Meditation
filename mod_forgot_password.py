# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import searchUser, generate_reset_token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from mod_db_account import send_reset_email, generate_random_password   

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = searchUser(email)
        
        if user:
            token = generate_reset_token(user['UserID'])
            send_reset_email(email, token)
            flash('A password reset link has been sent to your email.')
        else:
            flash('No account found with that email.')
    
    return render_template('forgot_password.html')


 