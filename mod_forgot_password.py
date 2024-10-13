from mod_utilize import app, session, redirect, url_for, request, flash, render_template
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from mod_db_account import search_user, generate_reset_token
from werkzeug.security import generate_password_hash
from db_baseOperation import execute_query  # Import execute_query

# Serializer to generate and validate tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        print(f"Received email: {email}")  # Debugging statement

        # Use execute_query to fetch user
        user = execute_query('SELECT * FROM users WHERE Email = %s', (email,), fetchone=True)

        if user:
            # Generate a secure token with the user's email
            print("User found, generating token")  # Debugging line
            token = serializer.dumps(email, salt='password-reset-salt')
            # Construct reset URL
            reset_url = url_for('reset_password', token=token, _external=True)
            print(f"Sending email to {email} with reset link: {reset_url}")  # Debugging line

            # Send reset password email using SendGrid
            message = Mail(
                from_email=os.environ.get('MAIL_USERNAME'),  # Your verified sender email
                to_emails=email,
                subject='Password Reset Request',
                html_content=f'<p>Click the link to reset your password: <a href="{reset_url}">{reset_url}</a></p>'
            )

            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                flash('A password reset link has been sent to your email.', 'info')
            except Exception as e:
                flash(f'Failed to send email: {str(e)}', 'danger')
                print(f"Email sending error: {e}")  # Debugging line
                if hasattr(e, 'body'):
                    print(e.body)  # Print detailed error message from SendGrid
        else:
            flash('Email not found.', 'danger')

    return render_template('forgot_password.html')
