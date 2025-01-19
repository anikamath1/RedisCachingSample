import mysql.connector
from mysql.connector import Error

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",       # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="test_db"    # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
