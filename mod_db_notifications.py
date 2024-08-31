from db_baseOperation import execute_query
from datetime import datetime

# Search notifications by UserID
def searchNotificationById(user_id, condition=""):
    query = """
        SELECT * 
        FROM Notifications 
        LEFT JOIN Users ON Notifications.UserID = Users.UserID 
        WHERE Notifications.UserID = %s
    """
    if condition:
        query += " AND " + condition
    result = execute_query(query, (user_id,), fetchone=False)
    return result

# List all notifications with an optional condition
def searchNotification(condition=""):
    query = """
        SELECT * 
        FROM Notifications 
        LEFT JOIN Users ON Notifications.UserID = Users.UserID
    """
    if condition:
        query += " WHERE " + condition
    result = execute_query(query, fetchone=False)
    return result

# Get unread notification count for a specific user
def getUnreadNotificationCount(user_id):
    query = """
        SELECT COUNT(*) AS count 
        FROM Notifications 
        WHERE UserID = %s AND Status = 0  -- Assuming Status 0 means unread
    """
    result = execute_query(query, (user_id,), fetchone=True)
    return result

# Get the total number of notifications
def getNotificationCount():
    query = "SELECT COUNT(*) AS count FROM Notifications"
    result = execute_query(query, fetchone=True)
    return result

# Insert a new notification record
def InsertNotification(notification_time, user_id, details):
    query = """
        INSERT INTO Notifications (NotificationTime, UserID, Details) 
        VALUES (%s, %s, %s)
    """
    data = (notification_time, user_id, details)
    result = execute_query(query, data)
    return result

# Mark a notification as read
def markNotificationRead(notification_id):
    query = "UPDATE Notifications SET Status = 1 WHERE NotificationID = %s"
    result = execute_query(query, (notification_id,))
    return result

# Search for a notification by user_id and details
def searchNotificationByDetails(user_id, details):
    query = """
        SELECT * 
        FROM Notifications 
        WHERE UserID = %s AND Details = %s
    """
    result = execute_query(query, (user_id, details), fetchone=True)
    return result





def get_user_notifications(user_id):
    """
    Fetch notifications for a given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing notification data.
    """
    query = """
    SELECT 
        NotificationID,
        Details,
        NotificationTime,
        Status
    FROM Notifications
    WHERE UserID = %s
    ORDER BY NotificationTime DESC;
    """
    try:
        result = execute_query(query, (user_id,))
        return result if result else []
    except Exception as e:
        print(f"Error fetching notifications for user {user_id}: {e}")
        return []
