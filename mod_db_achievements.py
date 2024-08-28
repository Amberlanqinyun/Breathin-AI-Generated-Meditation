from mod_db_dashboard import get_user_meditation_history
from db_baseOperation import execute_query

def get_user_achievements(user_id):
    """
    Fetch the achievements for a given user.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing achievement data.
    """
    query = """
    SELECT 
        AchievementID,
        Type,
        Description,
        AchievedAt
    FROM Achievements
    WHERE UserID = %s
    ORDER BY AchievedAt DESC;
    """
    result = execute_query(query, (user_id,))
    
    return result if result else []

def check_and_award_achievements(user_id):
    """Check if the user has met any achievement criteria and award achievements."""
    meditation_history = get_user_meditation_history(user_id)
    days_practiced = len(set([meditation['SessionDate'] for meditation in meditation_history]))
    total_meditation_time = sum([meditation['Duration'] for meditation in meditation_history if meditation['Duration']])

    # Achievement: First Meditation
    if days_practiced >= 1:
        award_achievement(user_id, 'First Meditation', 'Completed first meditation session')

    # Achievement: 3-Day Streak
    if days_practiced >= 3:
        award_achievement(user_id, '3-Day Streak', 'Completed meditation for 3 consecutive days')

    # Achievement: 10 Hours of Meditation
    if total_meditation_time >= 600:
        award_achievement(user_id, '10 Hours of Meditation', 'Completed 10 hours of meditation')



def award_achievement(user_id, achievement_type, description):
    """Insert achievement into database and notify the user."""
    existing_achievements = get_user_achievements(user_id)
    if not any(ach['Type'] == achievement_type for ach in existing_achievements):
        insert_achievement(user_id, achievement_type, description)
        insert_notification(user_id, f"Congratulations! You've earned a new achievement: {achievement_type}")
        
        
def insert_achievement(user_id, achievement_type, description):
    """
    Inserts a new achievement into the Achievements table.

    Args:
        user_id (int): The ID of the user who earned the achievement.
        achievement_type (str): The type of achievement.
        description (str): A description of the achievement.
    """
    query = """
    INSERT INTO Achievements (UserID, Type, Description, AchievedAt)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
    """
    data = (user_id, achievement_type, description)

    try:
        execute_query(query, data)
        print(f"Achievement '{achievement_type}' inserted for user {user_id}.")
    except Exception as e:
        print(f"Error inserting achievement for user {user_id}: {e}")



def insert_notification(user_id, details):
    """
    Inserts a new notification into the Notifications table.

    Args:
        user_id (int): The ID of the user to notify.
        details (str): The notification details/message.
    """
    query = """
    INSERT INTO Notifications (UserID, Details, NotificationTime, Status)
    VALUES (%s, %s, CURRENT_TIMESTAMP, 0)
    """
    data = (user_id, details)

    try:
        execute_query(query, data)
        print(f"Notification inserted for user {user_id}: {details}")
    except Exception as e:
        print(f"Error inserting notification for user {user_id}: {e}")




def get_user_achievements(user_id):
    """
    Fetch the achievements for a given user.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing user achievement data.
    """
    query = """
    SELECT 
        a.Type AS AchievementType,
        DATE_FORMAT(a.AchievedAt, '%Y-%m-%d') AS AchievedDate
    FROM Achievements a
    WHERE a.UserID = %s
    ORDER BY a.AchievedAt DESC;
    """
    result = execute_query(query, (user_id,))

    # Convert result to list of dictionaries with keys matching the template
    if result:
        return [
            {
                'AchievementType': row['AchievementType'],
                'AchievedDate': row['AchievedDate']
            } for row in result
        ]
    else:
        return []  # Ensure it returns a list, even if empty

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
        n.Details,
        DATE_FORMAT(n.NotificationTime, '%Y-%m-%d %H:%i:%s') AS NotificationTime
    FROM Notifications n
    WHERE n.UserID = %s
    ORDER BY n.NotificationTime DESC;
    """
    result = execute_query(query, (user_id,))

    # Convert result to list of dictionaries with keys matching the template
    if result:
        return [
            {
                'Details': row['Details'],
                'NotificationTime': row['NotificationTime']
            } for row in result
        ]
    else:
        return []  # Ensure it returns a list, even if empty