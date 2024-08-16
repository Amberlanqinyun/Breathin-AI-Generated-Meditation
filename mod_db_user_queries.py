from db_baseOperation import execute_query
from datetime import datetime, date

def addANewQueries(first_name, last_name, email, message, preferred_contact_type='email'):
    dateNow = datetime.now()
    current_day = dateNow.strftime('%Y-%m-%d %H:%M:%S')
    contact_us_query = """INSERT INTO contact_us (contact_time, first_name, last_name, email, contact_message, preferred_contact_type)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
    execute_query(contact_us_query, (current_day, first_name, last_name, email, message, preferred_contact_type))


def getUserQueries(condition=""):
    query = """SELECT message_id, contact_time, contact_us.first_name, contact_us.last_name, 
                      contact_us.email, contact_message, contact_us.admin_id, 
                      admin.first_name AS admin_first_name, response_message, response_time 
               FROM contact_us 
               LEFT JOIN admin ON contact_us.admin_id = admin.admin_id"""
    if condition != "":
        query = query + " WHERE " + condition
    result = execute_query(query)
    return result


def replyAQuery(admin_id, response_message, message_id):
    dateNow = datetime.now()
    current_day = dateNow.strftime('%Y-%m-%d %H:%M:%S')
    query = "UPDATE contact_us SET response_time = %s, response_message = %s, admin_id = %s WHERE message_id = %s"
    data = (current_day, response_message, admin_id, message_id)
    result = execute_query(query, data)
    return result


def getQueryDetails(message_id):
    query = "SELECT * FROM contact_us WHERE message_id = %s"
    data = (message_id,)
    result = execute_query(query, data, fetchone=True)
    return result



def getQueryNumberByUserId(user_id):
    query = """SELECT COUNT(user.user_id) AS count 
               FROM contact_us 
               JOIN user ON contact_us.email = user.email 
               WHERE user.user_id = {}""".format(user_id)
    result = execute_query(query, None, fetchone=True)
    return result
