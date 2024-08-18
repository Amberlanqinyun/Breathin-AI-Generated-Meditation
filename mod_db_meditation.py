from db_baseOperation import execute_query
from datetime import datetime

# Function to get meditation history for a specific user
def getMeditationHistory(user_id):
    query = """
    SELECT SessionDate, COUNT(*) as SessionCount
    FROM MeditationSessions
    WHERE UserID = %s
    GROUP BY SessionDate
    ORDER BY SessionDate ASC
    """
    result = execute_query(query, (user_id,))
    return result

# Function to get meditation achievements for a specific user
def getMeditationAchievements(user_id):
    query = """
    SELECT Type, Description, AchievedAt
    FROM Achievements
    WHERE UserID = %s
    ORDER BY AchievedAt DESC
    """
    result = execute_query(query, (user_id,))
    return result

# Function to check if a user has not meditated for a certain number of days
def getStreakNotifications(user_id, days_without_meditation=3):
    query = """
    SELECT MAX(SessionDate) as LastSessionDate
    FROM MeditationSessions
    WHERE UserID = %s
    """
    last_session = execute_query(query, (user_id,), fetchone=True)

    if last_session and last_session['LastSessionDate']:
        last_session_date = last_session['LastSessionDate']
        days_since_last_session = (datetime.now().date() - last_session_date).days
        if days_since_last_session >= days_without_meditation:
            return {
                'message': f"It has been {days_since_last_session} days since your last meditation session. Remember to meditate regularly for a better experience."
            }
    return None

# Function to add a new meditation session
def addMeditationSession(user_id, meditation_id, session_date=None):
    if session_date is None:
        session_date = datetime.now().date()

    query = """
    INSERT INTO MeditationSessions (UserID, MeditationID, SessionDate)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE SessionDate = VALUES(SessionDate)
    """
    result = execute_query(query, (user_id, meditation_id, session_date))
    return result

# Function to retrieve all meditations for a user
def getUserMeditations(user_id):
    query = """
    SELECT Meditations.MeditationID, Categories.Name as CategoryName, Meditations.TextContent, Meditations.AudioFilePath, Meditations.VisualContentPath, Meditations.CreatedAt
    FROM Meditations
    LEFT JOIN Categories ON Meditations.CategoryID = Categories.CategoryID
    WHERE Meditations.UserID = %s
    ORDER BY Meditations.CreatedAt DESC
    """
    result = execute_query(query, (user_id,))
    return result
