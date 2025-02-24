from datetime import datetime, timedelta
from db_baseOperation import execute_query  

# Function to retrieve all achievements for a user
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

def insert_meditation_session(user_id, meditation_id):
    """
    Insert a new meditation session into the MeditationSessions table.
    
    Args:
        user_id (int): The ID of the user.
        meditation_id (int): The ID of the meditation.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    query = """
    INSERT INTO MeditationSessions (UserID, MeditationID, SessionDateTime)
    VALUES (%s, %s, %s);
    """
    try:
        execute_query(query, (user_id, meditation_id, current_time))
        print(f"Meditation session for user {user_id} inserted successfully.")
        return True
    except Exception as e:
        print(f"Error inserting meditation session: {e}")
        return False

# Function to insert a new achievement into the database
def insert_achievement(user_id, achievement_type, description):
    """
    Insert a new achievement into the Achievements table.

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

# Function to insert a new notification for the user
def insert_notification(user_id, details):
    """
    Insert a new notification into the Notifications table.

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

# Function to calculate the user's streak of consecutive meditation days
def calculate_consecutive_days_streak(meditation_history):
    """
    Calculate the user's current streak of consecutive meditation days.
    
    Args:
        meditation_history (list): List of dictionaries containing meditation sessions.
    
    Returns:
        int: Number of consecutive days with meditation.
    """
    # Extract and sort dates from the session history
    dates = sorted(set(session['SessionDateTime'].date() for session in meditation_history))
    streak = 0
    current_streak = 0
    today = datetime.now().date()

    for i in range(len(dates) - 1, -1, -1):
        if i == len(dates) - 1:
            # Check if today is part of the streak
            if dates[i] == today:
                current_streak += 1
        else:
            # Check if each day in the list is consecutive
            if (dates[i + 1] - dates[i]).days == 1:
                current_streak += 1
            else:
                break  # Streak is broken

    return current_streak

# Function to calculate the number of meditation sessions per day for a user
def calculate_sessions_per_day(meditation_history):
    """
    Calculate the number of meditation sessions per day for a user.
    
    Args:
        meditation_history (list): List of dictionaries containing meditation sessions.
    
    Returns:
        dict: A dictionary where keys are dates and values are session counts.
    """
    sessions_per_day = {}
    
    for session in meditation_history:
        date = session['SessionDateTime'].date()
        if date in sessions_per_day:
            sessions_per_day[date] += 1
        else:
            sessions_per_day[date] = 1
    
    return sessions_per_day

# Function to award an achievement to a user
def award_achievement(user_id, achievement_type, description):
    """
    Insert achievement into the database and notify the user.
    
    Args:
        user_id (int): The ID of the user.
        achievement_type (str): The type of achievement.
        description (str): A description of the achievement.
    """
    # Check if the user already has this achievement
    try:
        existing_achievements = get_user_achievements(user_id)
        
        if not any(ach['Type'] == achievement_type for ach in existing_achievements):
            # If the user does not already have this achievement, insert it
            insert_achievement(user_id, achievement_type, description)
            # Insert a notification for the user about the new achievement
            insert_notification(user_id, f"Congratulations! You've earned a new achievement: {achievement_type}")
    except Exception as e:
        print(f"Error awarding achievement: {e}")

def get_user_meditation_history(user_id):
    """
    Fetch the meditation history for a given user in NZ date-time format.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing meditation session data.
    """
    query = """
    SELECT 
        m.SessionDateTime,
        me.TextContent AS MeditationName,
        me.AudioFilePath,
        m.MeditationID
    FROM MeditationSessions m
    JOIN Meditations me ON m.MeditationID = me.MeditationID
    WHERE m.UserID = %s
    ORDER BY m.SessionDateTime DESC;
    """
    
    try:
        # Fetch results using the execute_query function
        result = execute_query(query, (user_id,))

        if not result:
            print(f"No meditation history found for user {user_id}.")
            return []
        
        # Ensure correct data structure before processing
        formatted_result = []
        for row in result:
            try:
                formatted_result.append({
                    'SessionDateTime': row['SessionDateTime'],  # Use direct database column name
                    'MeditationName': row['MeditationName'],
                    'AudioFilePath': row['AudioFilePath'],
                    'MeditationID': row['MeditationID']
                })
            except KeyError as e:
                print(f"KeyError encountered: {e}. Row data: {row}")

        return formatted_result

    except Exception as e:
        print(f"Error occurred while fetching meditation history: {e}")
        return []

def has_achievement(user_id, achievement_type):
    """
    Check if the user already has a specific achievement.
    
    Args:
        user_id (int): The ID of the user.
        achievement_type (str): The type of achievement to check.

    Returns:
        bool: True if the user has the achievement, False otherwise.
    """
    achievements = get_user_achievements(user_id)
    return any(ach['Type'] == achievement_type for ach in achievements)


def prepare_heatmap_data(meditation_history):
    """
    Prepare data for heatmap visualization based on meditation history.

    Args:
        meditation_history (list): List of dictionaries containing meditation session data.

    Returns:
        dict: A dictionary with date keys and count of sessions per day for heatmap visualization.
    """
    heatmap_data = {}
    for session in meditation_history:
        session_date = session['SessionDateTime'].date()  # Extract the date part
        if session_date in heatmap_data:
            heatmap_data[session_date] += 1
        else:
            heatmap_data[session_date] = 1
    return heatmap_data