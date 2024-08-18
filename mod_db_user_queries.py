from datetime import datetime
from db_baseOperation import execute_query

# Function to add a new query to the ContactUs table
def addANewQueries(first_name, last_name, email, message):
    contact_us_query = """INSERT INTO ContactUs (FirstName, LastName, Email, Message)
                          VALUES (%s, %s, %s, %s)"""
    execute_query(contact_us_query, (first_name, last_name, email, message))

# Function to retrieve user queries with an optional condition
def getUserQueries(condition=""):
    query = """SELECT ContactID, SubmittedAt, ContactUs.FirstName, ContactUs.LastName, 
                      ContactUs.Email, Message, ContactUs.AdminID, 
                      Admins.FirstName AS AdminFirstName, ResponseMessage, ResponseTime 
               FROM ContactUs 
               LEFT JOIN Admins ON ContactUs.AdminID = Admins.AdminID"""
    if condition != "":
        query = query + " WHERE " + condition
    result = execute_query(query)
    return result

# Function to reply to a user query by updating the ContactUs table
def replyAQuery(admin_id, response_message, contact_id):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "UPDATE ContactUs SET ResponseTime = %s, ResponseMessage = %s, AdminID = %s WHERE ContactID = %s"
    data = (current_time, response_message, admin_id, contact_id)
    result = execute_query(query, data)
    return result

# Function to get the details of a specific query by its ID
def getQueryDetails(contact_id):
    query = "SELECT * FROM ContactUs WHERE ContactID = %s"
    data = (contact_id,)
    result = execute_query(query, data, fetchone=True)
    return result

# Function to get the number of queries submitted by a specific user
def getQueryNumberByUserId(user_id):
    query = """SELECT COUNT(Users.UserID) AS count 
               FROM ContactUs 
               JOIN Users ON ContactUs.Email = Users.Email 
               WHERE Users.UserID = %s"""
    result = execute_query(query, (user_id,), fetchone=True)
    return result
