import mysql.connector
from datetime import datetime, timedelta
import random
from db_credentials import db_config

# Establish a MySQL database connection
conn = mysql.connector.connect(
    host=db_config['db_host'],
    user=db_config['db_user'],
    password=db_config['db_password'],
    database=db_config['db_name'],
    port=db_config['port']
)

c = conn.cursor()

# Insert dummy data into Roles
roles_data = [
    ('Admin',),
    ('User',)
]
c.executemany('INSERT IGNORE INTO Roles (RoleName) VALUES (%s)', roles_data)

# Insert dummy data into Users
users_data = [
    ('John', 'Doe', 'john@example.com', 'hashed_password1', 2),  # User role
    ('Jane', 'Smith', 'jane@example.com', 'hashed_password2', 2),  # User role
    ('Admin', 'User', 'admin@example.com', 'hashed_password3', 1)  # Admin role
]
c.executemany('INSERT INTO Users (FirstName, LastName, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s, %s)', users_data)

# Insert dummy data into Admins
admins_data = [
    ('Alice', 'Admin', 'alice.admin@example.com', 'hashed_password4', 1),
    ('Bob', 'Admin', 'bob.admin@example.com', 'hashed_password5', 1)
]
c.executemany('INSERT INTO Admins (FirstName, LastName, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s, %s)', admins_data)

# Insert dummy data into Categories
categories_data = [
    ('Mindfulness', 'Mindfulness meditation helps focus on the present moment.'),
    ('Sleep', 'Guided meditations for better sleep.'),
    ('Stress Relief', 'Meditations to help manage stress.')
]
c.executemany('INSERT INTO Categories (Name, Description) VALUES (%s, %s)', categories_data)

# Retrieve UserID and CategoryID values from the Users and Categories tables
c.execute('SELECT UserID FROM Users')
user_ids = [row[0] for row in c.fetchall()]

c.execute('SELECT CategoryID FROM Categories')
category_ids = [row[0] for row in c.fetchall()]

# Insert dummy data into Meditations using valid CategoryID values
meditations_data = [
    (user_ids[0], category_ids[0], 'Mindfulness Session 1', '/path/to/audio1.mp3', '/path/to/visual1.jpg'),
    (user_ids[1], category_ids[1], 'Sleep Session 1', '/path/to/audio2.mp3', '/path/to/visual2.jpg'),
    (user_ids[2], category_ids[2], 'Stress Relief Session 1', '/path/to/audio3.mp3', '/path/to/visual3.jpg')
]
c.executemany('''
    INSERT INTO Meditations (UserID, CategoryID, TextContent, AudioFilePath, VisualContentPath)
    VALUES (%s, %s, %s, %s, %s)
''', meditations_data)

# Retrieve valid MeditationID values from the Meditations table
c.execute('SELECT MeditationID FROM Meditations')
meditation_ids = [row[0] for row in c.fetchall()]

# Function to generate a random date within a given range
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Insert dummy data into MeditationSessions
start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-08-01', '%Y-%m-%d')

meditation_sessions_data = []
for user_id in user_ids:  # Loop through existing user_ids
    session_count = random.randint(5, 20)
    session_dates = set()
    while len(session_dates) < session_count:
        session_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        session_dates.add(session_date)
    for session_date in session_dates:
        meditation_id = random.choice(meditation_ids)  # Use only valid MeditationIDs
        meditation_sessions_data.append((user_id, meditation_id, session_date))

c.executemany('''
    INSERT INTO MeditationSessions (UserID, MeditationID, SessionDate)
    VALUES (%s, %s, %s)
''', meditation_sessions_data)

# Insert dummy data into UserFeedback
feedback_data = [
    (user_ids[0], meditation_ids[0], 5, 'Very relaxing session.'),
    (user_ids[1], meditation_ids[1], 4, 'Helped me sleep better.'),
    (user_ids[2], meditation_ids[2], 3, 'It was okay, could be better.')
]
c.executemany('''
    INSERT INTO UserFeedback (UserID, MeditationID, Rating, Comments)
    VALUES (%s, %s, %s, %s)
''', feedback_data)

# Insert dummy data into UsageReports
usage_reports_data = [
    (user_ids[0], meditation_ids[0], '2023-07-01', 'High'),
    (user_ids[1], meditation_ids[1], '2023-07-02', 'Medium'),
    (user_ids[2], meditation_ids[2], '2023-07-03', 'Low')
]
c.executemany('''
    INSERT INTO UsageReports (UserID, MeditationID, SessionDate, EngagementLevel)
    VALUES (%s, %s, %s, %s)
''', usage_reports_data)

# Insert dummy data into Achievements
achievements_data = [
    (user_ids[0], 'Milestone', 'Completed 10 meditation sessions.'),
    (user_ids[1], 'Consistency', 'Meditated every day for a week.'),
    (user_ids[2], 'Stress Free', 'Reduced stress levels significantly.')
]
c.executemany('''
    INSERT INTO Achievements (UserID, Type, Description)
    VALUES (%s, %s, %s)
''', achievements_data)

# Insert dummy data into Subscriptions
subscriptions_data = [
    (user_ids[0], 'Monthly', '2023-06-01', '2023-07-01', 'Active'),
    (user_ids[1], 'Annual', '2023-01-01', '2024-01-01', 'Active'),
    (user_ids[2], 'Monthly', '2023-07-01', '2023-08-01', 'Inactive')
]
c.executemany('''
    INSERT INTO Subscriptions (UserID, PlanType, StartDate, EndDate, Status)
    VALUES (%s, %s, %s, %s, %s)
''', subscriptions_data)

# Insert dummy data into Payments
payments_data = [
    (user_ids[0], 9.99, 'Credit Card', '2023-06-01', 'Completed'),
    (user_ids[1], 99.99, 'PayPal', '2023-01-01', 'Completed'),
    (user_ids[2], 9.99, 'Credit Card', '2023-07-01', 'Failed')
]
c.executemany('''
    INSERT INTO Payments (UserID, Amount, PaymentMethod, PaymentDate, Status)
    VALUES (%s, %s, %s, %s, %s)
''', payments_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
