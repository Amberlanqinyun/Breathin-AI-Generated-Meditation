from mod_utilize import execute_query

# Fetch all users
def get_all_users():
    sql = "SELECT * FROM Users"
    return execute_query(sql)

# Get user by ID
def get_user_by_id(user_id):
    sql = "SELECT * FROM Users WHERE UserID = %s"
    return execute_query(sql, (user_id,), fetchone=True)

# Update user profile
def update_user_profile(user_id, first_name, last_name, email):
    sql = """
    UPDATE Users SET FirstName = %s, LastName = %s, Email = %s WHERE UserID = %s
    """
    execute_query(sql, (first_name, last_name, email, user_id))

# Ban/Unban user
def toggle_user_ban(user_id, ban_status):
    sql = "UPDATE Users SET banned = %s WHERE UserID = %s"
    execute_query(sql, (ban_status, user_id))
