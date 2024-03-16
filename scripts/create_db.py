import sqlite3

# Connect to the SQLite data_and_logs
conn = sqlite3.connect('../app/data_and_logs/database/database.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# Create the events table
cursor.execute('''
    CREATE TABLE events (
        id INTEGER PRIMARY KEY,
        title TEXT,
        details TEXT,
        location TEXT,
        event_date DATE,
        event_time TIME,
        creation_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create the event_attendees table for the many-to-many relationship
cursor.execute('''
    CREATE TABLE event_attendees (
        user_id INTEGER,
        event_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (event_id) REFERENCES events (id),
        PRIMARY KEY (user_id, event_id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
