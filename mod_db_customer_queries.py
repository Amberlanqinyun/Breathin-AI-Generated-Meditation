from db_baseOperation import execute_query
from datetime import datetime, date


def addANewQueries(first_name, last_name, phone_number, email, message,preferred_contact_type='email'):
    dateNow = datetime.now()
    current_day = dateNow.strftime('%Y-%m-%d %H:%M:%S')
    contact_us_query = """INSERT INTO contact_us (contact_time, first_name, last_name, phone_number, email, contact_message, preferred_contact_type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    execute_query(contact_us_query, (current_day, first_name, last_name, phone_number, email, message,preferred_contact_type))
   


def getCustomerQueries(condition=""):
    query = "select message_id,contact_time,contact_us.first_name,contact_us.last_name,contact_us.phone_number,contact_us.email,contact_message, contact_us.staff_id, staff.first_name as staff_first_name,  response_message, response_time from contact_us left join staff on contact_us.staff_id = staff.staff_id "
    if condition !="":
        query = query +" where "+condition
    result = execute_query(query)
    return result   


def replyAQuery(staff_id, reponse_message, message_id):
    dateNow = datetime.now()
    current_day = dateNow.strftime('%Y-%m-%d %H:%M:%S')
    query = "update contact_us  SET response_time = %s, response_message =%s, staff_id=%s WHERE message_id = %s"
    date =(current_day, reponse_message,staff_id, message_id)
    result = execute_query(query, date)
    return result   

def getQueryDetails(message_id):
    query = "select * from contact_us WHERE message_id = %s"
    date =( message_id)
    result = execute_query(query, date,True)
    return result   

def getQueryNumber():
    query = "select count(*) as count from contact_us"
    result = execute_query(query, None,True)
    return result  

def getQueryNumberByCustomerId(customer_id):
    query = "select count(customers.customer_id) as count from contact_us join customers on contact_us.email = customers.email where customers.customer_id ={}".format(customer_id)
    result = execute_query(query, None,True)
    return result