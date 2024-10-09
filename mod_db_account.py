import secrets
import string
from db_baseOperation import execute_query
from datetime import datetime, timedelta
import os
import smtplib
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pymysql
from flask import session, url_for
from flask_mail import Mail, Message
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_user_session_info():
    """Retrieve UserID and RoleID from the session."""
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    if user_id and role_id:
        return {'user_id': user_id, 'role_id': role_id}
    return None

def is_user_logged_in():
    """Check if the user is logged in by verifying UserID in the session."""
    return 'user_id' in session

def is_admin():
    """Check if the logged-in user is an Admin based on RoleID."""
    session_info = get_user_session_info()
    return session_info and session_info['role_id'] == 1

def is_user():
    """Check if the logged-in user is a regular user based on RoleID."""
    session_info = get_user_session_info()
    return session_info and session_info['role_id'] == 2


def listAllUsers(condition=""):
    query = "SELECT * FROM Users"
    if condition:
        query += " " + condition
    result = execute_query(query)
    return result

def search_user(email):
    query = "SELECT * FROM Users WHERE Email = %s"
    return execute_query(query, (email,), fetchone=True)

def searchUserById(user_id):
    query = """
    SELECT * FROM Users 
    LEFT JOIN Roles ON Roles.RoleID = Users.RoleID 
    WHERE UserID = %s
    """
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def create_user(first_name, last_name, email, password_hash=None, google_id=None, role_id=2):
    if google_id:
        # User is created via Google authentication
        query = """
        INSERT INTO Users (FirstName, LastName, Email, GoogleID, RoleID)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (first_name, last_name, email, google_id, role_id)
    else:
        # User is created via regular registration
        query = """
        INSERT INTO Users (FirstName, LastName, Email, PasswordHash, RoleID)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (first_name, last_name, email, password_hash, role_id)
    return execute_query(query, data, is_insert=True)

def deactivateUser(user_id):
    query = "UPDATE Users SET banned = '1' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def activateUser(user_id):
    query = "UPDATE Users SET banned = '0' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result


def update_user_password(user_id, new_password):
    # Hash the new password before storing it in the database
    password_hash = hash_password(new_password)
    
    query = """
    UPDATE Users 
    SET PasswordHash = %s 
    WHERE UserID = %s
    """
    data = (password_hash, user_id)
    
    try:
        execute_query(query, data)
        return True  # Indicating success
    except Exception as e:
        print(f"Error updating user password: {e}")
        return False  # Indicating failure

def deleteUser(user_id):
    query = "DELETE FROM Users WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result


def generate_reset_token(user_id):
    # Set token expiration to 1 hour from now
    expiration = datetime.now() + timedelta(hours=1)  # Token valid for 1 hour
    # Generate token logic here
    token = f"{user_id}-{int(expiration.timestamp())}"
    return token

def save_reset_token(user_id, token):
    query = "UPDATE Users SET reset_token = %s, token_expiry = DATE_ADD(NOW(), INTERVAL 1 HOUR) WHERE UserID = %s"
    execute_query(query, (token, user_id))


def verify_reset_token(token):
    query = "SELECT * FROM Users WHERE reset_token = %s AND token_expiry > NOW()"
    return execute_query(query, (token,), fetchone=True)

def get_user_profile(user_id):
    query = "SELECT FirstName, LastName, Email, PasswordHash FROM Users WHERE UserID = %s"
    return execute_query(query, (user_id,), fetchone=True)

def update_user_profile(first_name, last_name, email, user_id):
    query = "UPDATE Users SET FirstName = %s, LastName = %s, Email = %s WHERE UserID = %s"
    execute_query(query, (first_name, last_name, email, user_id))


def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(hashed_password, password):
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user(email, password):
    """Authenticate the user by checking the Users table."""
    user = search_user(email)  # Retrieve the user by email from the Users table
    
    if user:
        print(f"Hashed password in DB: '{user['PasswordHash']}'")
        print(f"Password entered by user: '{password}'")
        print(f"Password length: {len(password)}")
        is_match = check_password(user['PasswordHash'], password.strip())
        print(f"Bcrypt match result: {is_match}")  # Log bcrypt comparison result
        print(f"User banned status: {user['banned']}")
    # Check if user exists and verify password using bcrypt
    if user and is_match and not user['banned']:
        return user  # Return the user if authentication is successful
    else:
        print("Authentication failed")
    return None  # Return None if authentication fails

def generate_random_password(length=12):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

def send_reset_email(email, token):
    try:
        # Email content
        subject = "Password Reset Request"
        body = f"Please use the following link to reset your password: http://yourdomain.com/reset_password?token={token}"
        
        # Create the email
        message = MIMEText(body)
        message['to'] = email
        message['from'] = os.getenv('EMAIL_USER')
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Load credentials from environment variables
        credentials = Credentials(
            None,
            refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            token_uri='https://oauth2.googleapis.com/token'
        )

        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=credentials)

        # Send the email
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        
        print(f"Reset email sent to: {email}")  # Debugging statement
        print(f"Gmail API response: {message}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_user_by_email(email):
    query = "SELECT * FROM Users WHERE Email = %s"
    return execute_query(query, (email,), fetchone=True)

def update_user(user_id, first_name, last_name, email, google_id=None, password_hash=None):
    if google_id:
        # Update user with Google authentication
        query = """
        UPDATE Users
        SET FirstName = %s, LastName = %s, Email = %s, GoogleID = %s
        WHERE UserID = %s
        """
        data = (first_name, last_name, email, google_id, user_id)
    else:
        # Update user with regular registration
        query = """
        UPDATE Users
        SET FirstName = %s, LastName = %s, Email = %s, PasswordHash = %s
        WHERE UserID = %s
        """
        data = (first_name, last_name, email, password_hash, user_id)
    
    return execute_query(query, data)

