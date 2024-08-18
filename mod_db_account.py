from db_baseOperation import execute_query
from datetime import datetime, timedelta
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

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

def update_user_password(user_id, new_password):
    query = "UPDATE Users SET PasswordHash = %s WHERE UserID = %s"
    password_hash = hash_password(new_password)
    data = (password_hash, user_id)
    execute_query(query, data)

def update_admin_password(admin_id, new_password):
    query = "UPDATE Admins SET PasswordHash = %s WHERE AdminID = %s"
    password_hash = hash_password(new_password)
    data = (password_hash, admin_id)
    execute_query(query, data)
    
