import sqlite3
 #sqlite3 is a python library that knows how to work with SQLite databases.
 
conn = sqlite3.connect('notes.db')

#conn is a variable name where we store the connection
#notes.db is the database file we want to have

cursor = conn.cursor()
#create an assistant that(cursor) that talks to the database for me,whenever we want to create a atable or insert a note or delete it we'll tell the cursor not the database  
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    emotion TEXT,
    thoughts TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,email TEXT UNIQUE,password_hash TEXT)""")

conn.commit() #save all the changes
conn.close() #close the database connection


