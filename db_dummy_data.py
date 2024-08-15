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

# Create tables (if not already created)
c.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        RoleID INT AUTO_INCREMENT PRIMARY KEY,
        RoleName VARCHAR(50) UNIQUE NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(50) UNIQUE NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        PasswordHash VARCHAR(255) NOT NULL,
        RoleID INT NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
        StaffID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(50) UNIQUE NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        PasswordHash VARCHAR(255) NOT NULL,
        RoleID INT NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50) NOT NULL,
        Description TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Meditations (
        MeditationID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT NOT NULL,
        CategoryID INT,
        Category VARCHAR(50),
        TextContent TEXT,
        AudioFilePath VARCHAR(255),
        VisualContentPath VARCHAR(255),
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS MeditationSessions (
        SessionID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT NOT NULL,
        MeditationID INT NOT NULL,
        SessionDate DATE NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY (MeditationID) REFERENCES Meditations(MeditationID),
        UNIQUE (CustomerID, SessionDate)
    )
''')

# Insert dummy data into Roles
roles_data = [
    (1, 'Admin'),
    (2, 'User')
]
c.executemany('INSERT INTO Roles (RoleID, RoleName) VALUES (%s, %s) ON DUPLICATE KEY UPDATE RoleName = VALUES(RoleName)', roles_data)

# Insert dummy data into Customers
customers_data = [
    ('admin', 'admin@example.com', 'hashed_password', 1),
    ('john_doe', 'john@example.com', 'hashed_password', 2),
    ('jane_smith', 'jane@example.com', 'hashed_password', 2)
]
c.executemany('INSERT INTO Customers (Username, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s)', customers_data)

# Insert dummy data into Staff
staff_data = [
    ('staff1', 'staff1@example.com', 'hashed_password', 1),
    ('staff2', 'staff2@example.com', 'hashed_password', 1)
]
c.executemany('INSERT INTO Staff (Username, Email, PasswordHash, RoleID) VALUES (%s, %s, %s, %s)', staff_data)

# Insert dummy data into Categories
categories_data = [
    ('Mindfulness', 'Mindfulness meditation helps focus on the present moment.'),
    ('Sleep', 'Guided meditations for better sleep.'),
    ('Stress Relief', 'Meditations to help manage stress.')
]
c.executemany('INSERT INTO Categories (Name, Description) VALUES (%s, %s)', categories_data)

# Insert dummy data into Meditations
meditations_data = [
    (1, 1, 'Mindfulness', 'Mindfulness Session 1', '/path/to/audio1.mp3', '/path/to/visual1.jpg'),
    (2, 2, 'Sleep', 'Sleep Session 1', '/path/to/audio2.mp3', '/path/to/visual2.jpg'),
    (3, 3, 'Stress Relief', 'Stress Relief Session 1', '/path/to/audio3.mp3', '/path/to/visual3.jpg')
]
c.executemany('''
    INSERT INTO Meditations (CustomerID, CategoryID, Category, TextContent, AudioFilePath, VisualContentPath)
    VALUES (%s, %s, %s, %s, %s, %s)
''', meditations_data)

# Function to generate a random date within a given range
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Insert dummy data into MeditationSessions
start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-08-01', '%Y-%m-%d')

meditation_sessions_data = []
for customer_id in [1, 2, 3]:
    session_count = random.randint(5, 20)
    session_dates = set()
    while len(session_dates) < session_count:
        session_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        session_dates.add(session_date)
    for session_date in session_dates:
        meditation_id = random.choice([1, 2, 3])
        meditation_sessions_data.append((customer_id, meditation_id, session_date))

c.executemany('''
    INSERT INTO MeditationSessions (CustomerID, MeditationID, SessionDate)
    VALUES (%s, %s, %s)
''', meditation_sessions_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
