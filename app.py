from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# =========================
# DATABASE CONNECTION
# =========================
db = mysql.connector.connect(
    host="44.193.107.126",
    user="root",
    password="password",
    database="helpdesk"
)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# ABOUT
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# SIGNUP
# =========================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
        if cursor.fetchone():
            return "User already exists"

        cursor.execute("""
            INSERT INTO User (full_name, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, "user"))

        db.commit()
        return redirect("/login")

    return render_template("signup.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM User WHERE email=%s AND password=%s
        """, (email, password))

        user = cursor.fetchone()

        if user:
            session["user_id"] = user["user_id"]
            session["email"] = user["email"]
            session["name"] = user["full_name"]
            session["role"] = user.get("role", "user")

            return redirect("/tickets")

        return "Invalid login"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================
# VIEW TICKETS (ROLE BASED)
# =========================
@app.route("/tickets")
def tickets():
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    # FILTER VALUES
    status = request.args.get("status")
    priority = request.args.get("priority")
    category = request.args.get("category")

    query = """
        SELECT t.ticket_id, t.title, t.description,
               u.full_name, s.status_label, p.priority_level, c.category_label
        FROM Ticket t
        JOIN User u ON t.user_id = u.user_id
        JOIN Status s ON t.status_id = s.status_id
        JOIN Priority p ON t.priority_id = p.priority_id
        LEFT JOIN Category c ON t.category_id = c.category_id
        WHERE 1=1
    """

    params = []

    if session.get("role") != "admin":
        query += " AND t.user_id = %s"
        params.append(session["user_id"])

    if status:
        query += " AND s.status_label = %s"
        params.append(status)

    if priority:
        query += " AND p.priority_level = %s"
        params.append(priority)

    if category:
        query += " AND c.category_label = %s"
        params.append(category)

    cursor.execute(query, tuple(params))
    tickets = cursor.fetchall()

    for ticket in tickets:
        cursor.execute("""
            SELECT c.text, u.full_name
            FROM Comment c
            JOIN User u ON c.user_id = u.user_id
            WHERE c.ticket_id = %s
        """, (ticket["ticket_id"],))

        ticket["comments"] = cursor.fetchall()

    # LOAD FILTER DATA
    cursor.execute("SELECT * FROM Status")
    statuses = cursor.fetchall()

    cursor.execute("SELECT * FROM Priority")
    priorities = cursor.fetchall()

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    return render_template(
        "tickets.html",
        tickets=tickets,
        statuses=statuses,
        priorities=priorities,
        categories=categories
    )

# =========================
# CREATE TICKET
# =========================
@app.route("/create", methods=["GET", "POST"])
def create_ticket():
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category_id = request.form["category"]

        cursor.execute("""
            INSERT INTO Ticket (title, description, user_id, status_id, priority_id, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, description, session["user_id"], 1, 1, category_id))

        db.commit()
        return redirect("/tickets")

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    return render_template("create.html", categories=categories)
# =========================
# UPDATE TICKET (WITH PERMISSION)
# =========================
@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    # Check ownership
    cursor.execute("SELECT user_id FROM Ticket WHERE ticket_id=%s", (ticket_id,))
    owner = cursor.fetchone()

    if session.get("role") != "admin" and owner["user_id"] != session["user_id"]:
        return "Access denied"

    if request.method == "POST":
        status_id = request.form["status"]
        priority_id = request.form["priority"]
        category_id = request.form["category"]

        cursor.execute("""
            UPDATE Ticket
            SET status_id=%s, priority_id=%s, category_id=%s
            WHERE ticket_id=%s
        """, (status_id, priority_id, category_id, ticket_id))

        db.commit()
        return redirect("/tickets")

    # GET REQUEST
    cursor.execute("SELECT * FROM Ticket WHERE ticket_id=%s", (ticket_id,))
    ticket = cursor.fetchone()

    cursor.execute("SELECT * FROM Status")
    statuses = cursor.fetchall()

    cursor.execute("SELECT * FROM Priority")
    priorities = cursor.fetchall()

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()

    return render_template(
        "update.html",
        ticket=ticket,
        statuses=statuses,
        priorities=priorities,
        categories=categories
    )
# =========================
# DELETE TICKET
# =========================
@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    # Must be logged in
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    # Check if ticket exists
    cursor.execute("SELECT user_id FROM Ticket WHERE ticket_id=%s", (ticket_id,))
    owner = cursor.fetchone()

    if not owner:
        return "Ticket not found"

    # Check permission (admin OR owner)
    if session.get("role") != "admin" and owner["user_id"] != session["user_id"]:
        return "Access denied"

    try:
        cursor = db.cursor()

        # Delete related comments FIRST (prevents foreign key crash)
        cursor.execute("DELETE FROM Comment WHERE ticket_id=%s", (ticket_id,))

        # Delete the ticket
        cursor.execute("DELETE FROM Ticket WHERE ticket_id=%s", (ticket_id,))

        db.commit()

    except Exception as e:
        return f"Error deleting ticket: {e}"

    return redirect("/tickets")

# =========================
# ADD COMMENT (ADMIN ONLY)
# =========================
@app.route("/comment/<int:ticket_id>", methods=["POST"])
def add_comment(ticket_id):
    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return "Access denied"

    text = request.form["text"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO Comment (text, ticket_id, user_id)
        VALUES (%s, %s, %s)
    """, (text, ticket_id, session["user_id"]))

    db.commit()

    return redirect("/tickets")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)