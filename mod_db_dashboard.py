from db_baseOperation import execute_query
from datetime import datetime

def get_user_meditation_history(user_id):
    """
    Fetch the meditation history for a given user.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing meditation session data.
    """
    query = """
    SELECT 
        DATE_FORMAT(m.SessionDate, '%Y-%m-%d') AS SessionDate, 
        me.TextContent AS MeditationName,
        me.AudioFilePath,
        m.MeditationID
    FROM MeditationSessions m
    JOIN Meditations me ON m.MeditationID = me.MeditationID
    WHERE m.UserID = %s
    ORDER BY m.SessionDate DESC;
    """
    result = execute_query(query, (user_id,))

    # Convert result to list of dictionaries with keys matching the template
    if result:
        return [
            {
                'SessionDate': row['SessionDate'],
                'MeditationName': row['MeditationName'],
                'AudioFilePath': row['AudioFilePath'],
                'MeditationID': row['MeditationID']
            } for row in result
        ]
    else:
        return []  # Ensure it returns a list, even if empty



def get_user_usage_reports(user_id):
    """
    Fetch the usage reports for a given user.
    
    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing usage report data.
    """
    query = """
    SELECT 
        ReportID,
        MeditationID,
        SessionDate,
        EngagementLevel
    FROM UsageReports
    WHERE UserID = %s
    ORDER BY SessionDate DESC;
    """
    result = execute_query(query, (user_id,))
    
    return result if result else []


