from mod_utilize import execute_query

# Fetch all meditations t
def get_all_meditations(search_query=''):
    query = """
    SELECT Meditations.MeditationID, Meditations.TextContent, Categories.Name AS CategoryName
    FROM Meditations
    JOIN Categories ON Meditations.CategoryID = Categories.CategoryID
    WHERE Meditations.TextContent LIKE %s
    """
    search_term = f"%{search_query}%"
    return execute_query(query, (search_term,))

# Get meditation by ID
def get_meditation_by_id(meditation_id):
    sql = "SELECT * FROM Meditations WHERE MeditationID = %s"
    return execute_query(sql, (meditation_id,), fetchone=True)

# Insert a new meditation
def insert_meditation(category_id, text_content, audio_file_path):
    sql = """
    INSERT INTO Meditations (CategoryID, TextContent, AudioFilePath)
    VALUES (%s, %s, %s)
    """
    execute_query(sql, (category_id, text_content, audio_file_path))

# Update existing meditation
def update_meditation(meditation_id, text_content, audio_file_path):
    sql = """
    UPDATE Meditations
    SET TextContent = %s, AudioFilePath = %s
    WHERE MeditationID = %s
    """
    execute_query(sql, (text_content, audio_file_path, meditation_id))

# Delete a meditation
def delete_meditation(meditation_id):
    sql = "DELETE FROM Meditations WHERE MeditationID = %s"
    execute_query(sql, (meditation_id,))





