from db_baseOperation import execute_query
from datetime import datetime
import hashlib

def searchStaff(email):
    query = "SELECT * FROM staff WHERE email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchStaffById(id):
    query = "SELECT * FROM staff left join roles on roles.role_id = staff.role_id WHERE staff_id = %s"
    result = execute_query(query, (id,), fetchone=True)
    return result

def listAllStaffs(condition = ""):
    query = "select * from staff left join roles on roles.role_id = staff.role_id"
    if condition !="":
        query = query +" "+condition
    result = execute_query(query)
    return result

def listAllCustomers(condition = ""):
    query = "select * from customers"
    if condition !="":
        query = query +" "+condition
    result = execute_query(query)     
    return result

def searchCustomer(email):
    query = "SELECT * FROM customers WHERE email = %s"
    result = execute_query(query, (email,), fetchone=True)
    return result

def searchCustomerById(id):
    query = "SELECT * FROM customers left join roles on roles.role_id = customers.role_id WHERE customer_id = %s"
    result = execute_query(query, (id,), fetchone=True)
    return result

def insertCustomer(first_name, last_name, phone_number, email, password, address, date_of_birth, banned=False, news="", role_id = '1'):
    query = "INSERT INTO customers(first_name, last_name, phone_number, email, password, address, date_of_birth, banned, news,role_id) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (first_name, last_name, phone_number, email, password,address, date_of_birth,banned,news,role_id)
    result = execute_query(query, data)
    return result


def insertStaff(role_id, first_name, last_name, phone_number, email, password, employment_start_date=datetime.now().date(), news=""):
    query = "INSERT INTO staff(role_id, first_name, last_name, phone_number, email, password, employment_start_date,news) VALUES( %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (role_id, first_name, last_name, phone_number,email, password, employment_start_date, news)
    result = execute_query(query, data)
    return result


def deactiveCustomer(customer_id):
    query = "UPDATE customers SET banned='1' where customer_id = %s"
    result = execute_query(query, (customer_id,), fetchone=True)
    return result


def activeCustomer(customer_id):
    query = "UPDATE customers SET banned='0' where customer_id = %s"
    result = execute_query(query, (customer_id,), fetchone=True)
    return result


def update_staff_details(first_name, last_name, phone_number, email, staff_id):
    query = "UPDATE staff SET first_name = %s, last_name = %s, phone_number = %s, email = %s  WHERE staff_id = %s"
    data = (first_name, last_name, phone_number, email,staff_id)
    result = execute_query(query, data)
    return result


def update_customer_details(first_name, last_name, phone_number, email,address, customer_id):
    query = "UPDATE customers SET first_name = %s, last_name = %s, phone_number = %s, email = %s ,address = %s WHERE customer_id = %s"
    data = (first_name, last_name, phone_number, email, address,customer_id)
    result = execute_query(query, data)
    return result


def update_customer_password(user_id, new_password):
    # Prepare the query and data
    query = "UPDATE customers SET password = %s WHERE customer_id = %s"
    data = (new_password, user_id)
    # Execute the query
    execute_query(query, data)
    

def update_password(user_id, new_password):   
    # Prepare the query and data
    query = "UPDATE staff SET password = %s WHERE staff_id = %s"
    data = (new_password, user_id)
    # Execute the query
    execute_query(query, data)

# Function to hash passwords
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def deleteStaff(staff_id):
    query = "delete from staff  WHERE staff_id = %s"
    result = execute_query(query, (staff_id,), fetchone=True)
    return result


def deleteCustomer(customer_id):
    query = "delete from customers WHERE customer_id = %s"
    result = execute_query(query, (customer_id,), fetchone=True)
    return result


