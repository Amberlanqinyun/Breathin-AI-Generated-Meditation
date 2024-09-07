from db_baseOperation import execute_query
from datetime import datetime, timedelta
import os
import smtplib
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import session

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


def searchAdmin(email):
    query = "SELECT * FROM Admins WHERE Email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchAdminById(admin_id):
    query = """
    SELECT * FROM Admins 
    LEFT JOIN Roles ON Roles.RoleID = Admins.RoleID 
    WHERE AdminID = %s
    """
    result = execute_query(query, (admin_id,), fetchone=True)
    return result

def listAllAdmins(condition=""):
    query = """
    SELECT * FROM Admins 
    LEFT JOIN Roles ON Roles.RoleID = Admins.RoleID
    """
    if condition:
        query += " " + condition
    result = execute_query(query)
    return result

def listAllUsers(condition=""):
    query = "SELECT * FROM Users"
    if condition:
        query += " " + condition
    result = execute_query(query)
    return result

def searchUser(email):
    query = "SELECT * FROM Users WHERE Email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchUserById(user_id):
    query = """
    SELECT * FROM Users 
    LEFT JOIN Roles ON Roles.RoleID = Users.RoleID 
    WHERE UserID = %s
    """
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def insertUser(first_name, last_name, email, password, role_id='2'):
    query = """
    INSERT INTO Users (FirstName, LastName, Email, PasswordHash, RoleID) 
    VALUES (%s, %s, %s, %s, %s)
    """
    password_hash = hash_password(password)
    data = (first_name, last_name, email, password_hash, role_id)
    try:
        execute_query(query, data)
        return True  # Indicating success
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False  # Indicating failure


def insertAdmin(first_name, last_name, email, password, role_id='1'):
    query = """
    INSERT INTO Admins (FirstName, LastName, Email, PasswordHash, RoleID) 
    VALUES (%s, %s, %s, %s, %s)
    """
    password_hash = hash_password(password)
    data = (first_name, last_name, email, password_hash, role_id)
    result = execute_query(query, data)
    return result

def deactivateUser(user_id):
    query = "UPDATE Users SET banned = '1' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def activateUser(user_id):
    query = "UPDATE Users SET banned = '0' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def update_admin_details(first_name, last_name, email, admin_id):
    query = """
    UPDATE Admins 
    SET FirstName = %s, LastnNme = %s, Email = %s 
    WHERE AdminID = %s
    """
    data = (first_name, last_name, email, admin_id)
    result = execute_query(query, data)
    return result

def update_user_details(first_name, last_name, email, user_id):
    query = """
    UPDATE Users 
    SET FirstName = %s, LastName = %s, Email = %s 
    WHERE UserID = %s
    """
    data = (first_name, last_name, email, user_id)
    result = execute_query(query, data)
    return result

def deleteAdmin(admin_id):
    query = "DELETE FROM Admins WHERE AdminID = %s"
    result = execute_query(query, (admin_id,), fetchone=True)
    return result

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

def update_user_profile(user_id, first_name, last_name, email):
    query = "UPDATE Users SET FirstName = %s, LastName = %s, Email = %s WHERE UserID = %s"
    execute_query(query, (first_name, last_name, email, user_id))

def update_user_password(user_id, new_password_hash):
    query = "UPDATE Users SET PasswordHash = %s WHERE UserID = %s"
    execute_query(query, (new_password_hash, user_id))


def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def check_password(hashed_password, password):
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
