from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        first_name TEXT,
        last_name TEXT,
        middle_name TEXT,
        course_level TEXT,
        email TEXT,
        course TEXT,
        address TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():

    student_id = request.form["student_id"]
    password = request.form["password"]

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE student_id=? AND password=?",
        (student_id, password)
    ).fetchone()

    if user:
        session["user_id"] = user["id"]
        return redirect("/dashboard")
    else:
        return """
        <script>
        alert("Invalid ID or Password")
        window.location='/'
        </script>
        """


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():

    student_id = request.form["student_id"]
    last_name = request.form["last_name"]
    first_name = request.form["first_name"]
    middle_name = request.form["middle_name"]
    course_level = request.form["course_level"]
    email = request.form["email"]
    course = request.form["course"]
    address = request.form["address"]
    password = request.form["password"]

    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM users WHERE student_id=?",
        (student_id,)
    ).fetchone()

    if existing:
        return """
        <script>
        alert("Account already registered")
        window.location='/register'
        </script>
        """

    conn.execute("""
    INSERT INTO users
    (student_id,last_name,first_name,middle_name,course_level,email,course,address,password)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(
        student_id,last_name,first_name,middle_name,
        course_level,email,course,address,password
    ))

    conn.commit()
    conn.close()

    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)