# Import various modules created for and used in this python script
from mod_utilize import app, session, redirect, url_for, request, flash, render_template
import hashlib
from mod_db_account import searchUser, generate_reset_token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_reset_email(email, token):
    sender_email = "amber.lan.breath.in@gmail.com"
    receiver_email = email
    password = os.getenv("EMAIL_PASSWORD")


    # Create the email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = receiver_email

    reset_url = f"http://localhost:5000/reset_password?token={token}"

    text = f"""\
    Hi,
    To reset your password, please click the link below:
    {reset_url}
    If you did not request a password reset, please ignore this email.
    """
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

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


 