from mod_utilize import execute_query

# Fetch all users
def get_all_users():
    sql = "SELECT * FROM Users"
    return execute_query(sql)

# Get user by ID
def get_user_by_id(user_id):
    sql = "SELECT * FROM Users WHERE UserID = %s"
    return execute_query(sql, (user_id,), fetchone=True)

# Get user by email
def get_user_by_email(email):
    sql = "SELECT * FROM Users WHERE Email = %s"
    return execute_query(sql, (email,), fetchone=True)

# Update user profile
def update_user_profile(user_id, first_name, last_name, email):
    sql = """
    UPDATE Users SET FirstName = %s, LastName = %s, Email = %s WHERE UserID = %s
    """
    execute_query(sql, (first_name, last_name, email, user_id))

# Update user password
def update_user_password(user_id, new_password):
    sql = """
    UPDATE Users SET Password = %s WHERE UserID = %s
    """
    execute_query(sql, (new_password, user_id))

# Verify reset token
def verify_reset_token(token):
    # Your logic to verify the reset token
    pass

# Generate reset token
def generate_reset_token(user_id):
    # Your logic to generate a reset token
    pass

# Search user by email
def searchUser(email):
    return get_user_by_email(email)

# Ban/Unban user
def toggle_user_ban(user_id, ban_status):
    sql = "UPDATE Users SET banned = %s WHERE UserID = %s"
    execute_query(sql, (ban_status, user_id))
