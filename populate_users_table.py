import mysql.connector
import random

# Connect to MySQL
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )

# Populate the `users` table with 100,000 entries
def populate_users_table():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    print("Populating the users table with 100,000 entries...")
    cursor.execute("""
       DROP TABLE users
       """)
    # Create the table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
    """)
    connection.commit()

    # Insert 100,000 entries into the `users` table
    users = [
        (f"User {i}", f"user{i}@example.com", random.randint(18, 60))
        for i in range(1, 100001)
    ]
    cursor.executemany("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", users)
    connection.commit()

    print("Successfully added 100,000 entries to the users table.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    populate_users_table()
