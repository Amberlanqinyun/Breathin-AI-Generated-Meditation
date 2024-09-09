from db_baseOperation import execute_query
from datetime import datetime

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

# Function to get all meditation categories
def getMeditationCategories():
    query = """
    SELECT CategoryID, Name, Description
    FROM Categories
    ORDER BY Name ASC
    """
    result = execute_query(query)
    return result

def get_meditation_by_id(category_id):
    query = "SELECT * FROM Meditations WHERE CategoryID = %s"
    result = execute_query(query, (category_id,))
    if result:
        return result[0]
    return None


def get_meditation_by_category(category_id):
    query = 'SELECT * FROM Meditations WHERE CategoryID = %s'
    # Fetch all meditations for the given category
    return execute_query(query, data=(category_id,), fetchone=False)  # Set fetchone to False to fetch all records

def insert_user_feedback(user_id, meditation_id, rating, comments):
    query = 'INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments) VALUES (%s, %s, %s, %s)'
    execute_query(query, data=(user_id, meditation_id, rating, comments))
    
def get_meditation_by_id(meditation_id):
    query = "SELECT * FROM Meditations WHERE MeditationID = %s"
    result = execute_query(query, (meditation_id,), fetchone=True)  # Ensure fetchone is True here

    if result:
        return result  # Fetch one meditation, return directly
    else:
        return None


def search_meditations(query):
    """
    Search for meditations and include category names.
    """
    search_query = f"%{query}%"
    sql = """
    SELECT Meditations.MeditationID, Categories.Name AS CategoryName, Meditations.TextContent, Meditations.AudioFilePath, Meditations.VisualContentPath, Meditations.CreatedAt
    FROM Meditations
    LEFT JOIN Categories ON Meditations.CategoryID = Categories.CategoryID
    WHERE Meditations.TextContent LIKE %s
    ORDER BY Meditations.CreatedAt DESC
    """
    result = execute_query(sql, (search_query,), fetchone=False)  # Fetch all matching results
    return result


