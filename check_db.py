import sqlite3

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM notes")
notes = cursor.fetchall()

print(notes)

conn.close()