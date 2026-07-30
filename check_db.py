import sqlite3

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

print("----- USERS TABLE -----")

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(user)

conn.close()