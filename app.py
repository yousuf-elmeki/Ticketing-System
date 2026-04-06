from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# DB CONNECTION
db = mysql.connector.connect(
    host="44.193.107.126",
    user="root",
    password="password",
    database="helpdesk"
)

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")

# VIEW TICKETS (JOIN REQUIRED)
@app.route("/tickets")
def tickets():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT t.ticket_id, t.title, t.description,
               u.full_name, s.status_label, p.priority_level
        FROM Ticket t
        JOIN User u ON t.user_id = u.user_id
        JOIN Status s ON t.status_id = s.status_id
        JOIN Priority p ON t.priority_id = p.priority_id
    """)

    tickets = cursor.fetchall()
    return render_template("tickets.html", tickets=tickets)

# CREATE
@app.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        try:
            title = request.form["title"]
            description = request.form["description"]

            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO Ticket (title, description, user_id, status_id, priority_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, description, 1, 1, 1))

            db.commit()
            return redirect("/tickets")

        except:
            return render_template("error.html")

    return render_template("create.html")

# UPDATE
@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        try:
            status_id = request.form["status"]
            priority_id = request.form["priority"]

            cursor.execute("""
                UPDATE Ticket
                SET status_id = %s, priority_id = %s
                WHERE ticket_id = %s
            """, (status_id, priority_id, ticket_id))

            db.commit()
            return redirect("/tickets")

        except:
            return render_template("error.html")

    cursor.execute("SELECT * FROM Ticket WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()

    cursor.execute("SELECT * FROM Status")
    statuses = cursor.fetchall()

    cursor.execute("SELECT * FROM Priority")
    priorities = cursor.fetchall()

    return render_template("update.html", ticket=ticket, statuses=statuses, priorities=priorities)

# DELETE
@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Ticket WHERE ticket_id = %s", (ticket_id,))
        db.commit()
        return redirect("/tickets")
    except:
        return render_template("error.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)