from db_baseOperation import execute_query
from datetime import datetime, date


#seachNotification by cutomer_id
def searchNotificationById(customer_id, condition=""):
    query = "SELECT * FROM notification left join customers on notification.customer_id = customers.customer_id WHERE notification.customer_id = '{}' ".format(customer_id)
    if condition !="":
        query = query +" and "+condition
    result = execute_query(query, fetchone=False)
    return result

#list all the notification
def searchNotification( condition=""):
    query = "SELECT * FROM notification left join customers on notification.customer_id = customers.customer_id "
    if condition !="":
        query = query +" where "+condition
    result = execute_query(query, fetchone=False)
    return result

#get unread notificationcount
def getUnreadNotificationCount(customer_id):
    query = "SELECT count(*) as count FROM notification WHERE customer_id = %s group by customer_id "
    result = execute_query(query, (customer_id,), fetchone=True)
    print(result)
    return result
    

#get the totle number of notification
def getNotificationCount():
    query = "SELECT count(*) as count FROM notification"
    result = execute_query(query, fetchone=True)
    return result

#insert one record into notification table
def InsertNotification(notification_time, customer_id, details):
    query = "INSERT INTO notification ( notification_time, customer_id, details) VALUES (%s, %s, %s)"
    data = (notification_time, customer_id, details)         
    result = execute_query(query, data)
    return result

def markNotificationReaded(notification_id):
    query = "UPDATE customers SET status='1' where notification_id = %s"
    result = execute_query(query, (notification_id,), fetchone=True)
    return result

def searchNotificationByDetails(customer_id, details):
    query = "select * from notification where customer_id ='{}' and details = '{}' ".format(customer_id, details)
    result = execute_query(query)
    return result


def send_overdue_notifications():
    # 1. Identify all the overdue hireages.
    overdue_hireages = get_overdue_hireages()
    
    for hireage in overdue_hireages:
        customer_id = hireage['customer_id']
        # Constructing the overdue notification message.
        details = "Your hireage with order ID {} is overdue! Please return the items or contact us for assistance.".format(hireage['order_id'])
        notification_time = datetime.now()

        # 2. Insert the notification into the database.
        result = searchNotificationByDetails(customer_id,details)
        if not result:
            InsertNotification(notification_time, customer_id, details)
       

def get_overdue_hireages():
    current_time = datetime.now()
    query = """
    SELECT order_id, customer_id FROM orders 
    WHERE return_due_time < %s AND order_status_id != 3 
    """ 
    result = execute_query(query, (current_time,), fetchone=False)
    return result

