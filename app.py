from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# 🔹 DATABASE CONNECTION FUNCTION
def get_db_connection():
    return mysql.connector.connect(
        host="44.193.107.126",
        user="root",
        password="password",
        database="helpdesk"
    )

# -------- ROUTES --------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/tickets")
def tickets():
    db = get_db_connection()
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

    cursor.close()
    db.close()

    return render_template("tickets.html", tickets=tickets)



@app.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO Ticket (title, description, user_id, status_id, priority_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, 1, 1, 1))

        db.commit()

        cursor.close()
        db.close()

        return redirect("/tickets")

    return render_template("create.html")



@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        status_id = request.form["status"]
        priority_id = request.form["priority"]

        cursor.execute("""
            UPDATE Ticket
            SET status_id = %s, priority_id = %s
            WHERE ticket_id = %s
        """, (status_id, priority_id, ticket_id))

        db.commit()
        db.close()

        return redirect("/tickets")

    # GET request
    cursor.execute("SELECT * FROM Ticket WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()

    cursor.execute("SELECT * FROM Status")
    statuses = cursor.fetchall()

    cursor.execute("SELECT * FROM Priority")
    priorities = cursor.fetchall()

    db.close()

    return render_template(
        "update.html",
        ticket=ticket,
        statuses=statuses,
        priorities=priorities
    )


@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Ticket WHERE ticket_id = %s", (ticket_id,))
    db.commit()

    db.close()

    return redirect("/tickets")

# -------- RUN APP --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)