import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",      # or 127.0.0.1
    user="root",            # your MySQL username (usually 'root')
    password="Aman@123",# your MySQL password (put it inside quotes)
    database="food_ordering_system"
)

# Create a cursor object
cursor = conn.cursor()

# Simple check
cursor.execute("SHOW TABLES;")
for table in cursor.fetchall():
    print(table)

# Always good to close when done
conn.close()
