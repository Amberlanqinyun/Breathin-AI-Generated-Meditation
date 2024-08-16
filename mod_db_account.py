from db_baseOperation import execute_query
from datetime import datetime
import hashlib

def searchAdmin(email):
    query = "SELECT * FROM Admin WHERE Email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchAdminById(id):
    query = "SELECT * FROM Admin LEFT JOIN Roles ON Roles.RoleID = Admin.RoleID WHERE AdminID = %s"
    result = execute_query(query, (id,), fetchone=True)
    return result

def listAllAdmins(condition=""):
    query = "SELECT * FROM Admin LEFT JOIN Roles ON Roles.RoleID = Admin.RoleID"
    if condition != "":
        query += " " + condition
    result = execute_query(query)
    return result

def listAllUsers(condition=""):
    query = "SELECT * FROM User"
    if condition != "":
        query += " " + condition
    result = execute_query(query)
    return result

def searchUser(email):
    query = "SELECT * FROM User WHERE Email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchUserById(id):
    query = "SELECT * FROM User LEFT JOIN Roles ON Roles.RoleID = User.RoleID WHERE UserID = %s"
    result = execute_query(query, (id,), fetchone=True)
    return result

def insertUser(first_name, last_name, email, password, role_id='2'):
    query = "INSERT INTO User (Firstname, Lastname, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s, %s)"
    data = (first_name, last_name, email, password, role_id)
    result = execute_query(query, data)
    return result

def insertAdmin(role_id, first_name, last_name, email, password, employment_start_date=datetime.now().date()):
    query = "INSERT INTO Admin (RoleID, Firstname, Lastname, Email, PasswordHash, EmploymentStartDate) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (role_id, first_name, last_name, email, password, employment_start_date)
    result = execute_query(query, data)
    return result

def deactivateUser(user_id):
    query = "UPDATE User SET Banned='1' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def activateUser(user_id):
    query = "UPDATE User SET Banned='0' WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result

def update_admin_details(first_name, last_name, email, admin_id):
    query = "UPDATE Admin SET Firstname = %s, Lastname = %s, Email = %s WHERE AdminID = %s"
    data = (first_name, last_name, email, admin_id)
    result = execute_query(query, data)
    return result

def update_user_details(first_name, last_name, email, user_id):
    query = "UPDATE User SET Firstname = %s, Lastname = %s, Email = %s WHERE UserID = %s"
    data = (first_name, last_name, email, user_id)
    result = execute_query(query, data)
    return result

def update_user_password(user_id, new_password):
    query = "UPDATE User SET PasswordHash = %s WHERE UserID = %s"
    data = (new_password, user_id)
    execute_query(query, data)

def update_admin_password(admin_id, new_password):
    query = "UPDATE Admin SET PasswordHash = %s WHERE AdminID = %s"
    data = (new_password, admin_id)
    execute_query(query, data)

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def deleteAdmin(admin_id):
    query = "DELETE FROM Admin WHERE AdminID = %s"
    result = execute_query(query, (admin_id,), fetchone=True)
    return result

def deleteUser(user_id):
    query = "DELETE FROM User WHERE UserID = %s"
    result = execute_query(query, (user_id,), fetchone=True)
    return result
