from flask import Flask, render_template, request,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
#Import the function that converts the real password into a secure hash
import sqlite3
app = Flask(__name__)
app.secret_key = "something"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print("Email entered:", email)
        print("Password entered:", password)
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
        user = cursor.fetchone()
        print("User from DB:", user)
#what is user now:2 chances-one is when email exixtes and other is when not existed
    #so if its case 2 we write this
        if not user:
            conn.close()
            return "Email does not exist"
        if not check_password_hash(user[3], password):
            conn.close()
            return "Incorrect password"
        session["user_id"] = user[0]
        conn.close()
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route('/dashboard')
def dashboard():
    
    if "user_id" not in session:
        return redirect("/login")

    return render_template('dashboard.html')

@app.route('/new-note', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form.get('title')
        thoughts = request.form.get('thoughts')
        emotion = request.form.get("emotion")
        
        user_id = session["user_id"]
        
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notes(user_id, title, emotion, thoughts)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, emotion, thoughts))
        conn.commit()
        conn.close()
        return redirect("/notes")
    return render_template('new_notes.html')

@app.route('/notes')
def all_notes():
    if "user_id" not in session:
        return redirect("/login")
    
    conn =sqlite3.connect('notes.db')
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM notes WHERE user_id = ?",
        (session["user_id"],)
    )
    notes = cursor.fetchall()
    conn.close()
    return render_template('notes.html',notes=notes)
  #left side notes is the name of html/jinga that we use and rightside one
  #is the python variable we created using fetchall()
  
@app.route("/view-note/<int:id>")#whatever the ID comes in the URL,store it in the python variable id
def view_note(id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute(
    "SELECT * FROM notes WHERE id=? AND user_id=?",
    (id, session["user_id"]))
    note = cursor.fetchone()
    conn.close()
    return render_template("view_note.html",note=note)


@app.route("/edit-note/<int:id>")
def edit_note(id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute(
    "SELECT * FROM notes WHERE id=? AND user_id=?",
    (id, session["user_id"]))
    note = cursor.fetchone()
    conn.close()
    return render_template("edit_note.html",note=note)


@app.route("/update-note/<int:id>", methods=["POST"])
def update_note(id):
    title = request.form["title"]
    emotion = request.form["emotion"]
    thoughts = request.form["thoughts"]

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notes
        SET title=?, emotion=?, thoughts=?
        WHERE id=? AND user_id=?
    """, (title, emotion, thoughts, id,session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/notes")

@app.route("/delete-note/<int:id>")
def delete_note(id):

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    
    cursor.execute(
    "DELETE FROM notes WHERE id=? AND user_id=?",
    (id, session["user_id"]))
    
    conn.commit()
    conn.close()

    return redirect("/notes")

#User fills the form    
#POST request     
#Flask receives username, email, password, confirm_password       
#Check passwords match      
#Generate password hash      
#Insert username, email, password_hash into users table     
#Commit
#Close connection 
#Redirect to Login 

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match"

        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
        user = cursor.fetchone()
        #Store the matching user if found; otherwise store None.
        if user: #If a user with this email already exists...
            conn.close() #Close the database connection
            return "Email already exists"
        # Check username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return "Username already exists"
    #insert new user
        cursor.execute("""INSERT INTO users(username, email, password_hash) VALUES (?, ?, ?)""",(username, email, password_hash))

        conn.commit()
        conn.close()

        # After successful registration
        return redirect("/login")
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)