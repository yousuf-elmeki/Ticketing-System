from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# -------------------------
# DATABASE CONNECTION FUNCTION
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="44.193.107.126",
        user="root",
        password="password",
        database="helpdesk"
    )

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# ABOUT
# -------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------
# VIEW TICKETS
# -------------------------
@app.route("/tickets")
def tickets():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT t.ticket_id, t.title, t.description,
                   u.full_name, s.status_label, p.priority_level
            FROM Ticket t
            JOIN User u ON t.user_id = u.user_id
            JOIN Status s ON t.status_id = s.status_id
            JOIN Priority p ON t.priority_id = p.priority_id
        """)

        tickets = cursor.fetchall()
        conn.close()

        return render_template("tickets.html", tickets=tickets)

    except Exception as e:
        return f"Error loading tickets: {str(e)}"

# -------------------------
# CREATE TICKET
# -------------------------
@app.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        try:
            title = request.form["title"]
            description = request.form["description"]

            conn = get_db_connection()
            cursor = conn.cursor()

            # Make sure these IDs exist in your database
            cursor.execute("""
                INSERT INTO Ticket (title, description, user_id, status_id, priority_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, description, 1, 1, 1))

            conn.commit()
            conn.close()

            return redirect("/tickets")

        except Exception as e:
            return f"Error creating ticket: {str(e)}"

    return render_template("create.html")

# -------------------------
# UPDATE TICKET
# -------------------------
@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == "POST":
            status_id = request.form["status"]
            priority_id = request.form["priority"]

            cursor.execute("""
                UPDATE Ticket
                SET status_id = %s, priority_id = %s
                WHERE ticket_id = %s
            """, (status_id, priority_id, ticket_id))

            conn.commit()
            conn.close()

            return redirect("/tickets")

        cursor.execute("SELECT * FROM Ticket WHERE ticket_id = %s", (ticket_id,))
        ticket = cursor.fetchone()

        cursor.execute("SELECT * FROM Status")
        statuses = cursor.fetchall()

        cursor.execute("SELECT * FROM Priority")
        priorities = cursor.fetchall()

        conn.close()

        return render_template("update.html",
                               ticket=ticket,
                               statuses=statuses,
                               priorities=priorities)

    except Exception as e:
        return f"Error updating ticket: {str(e)}"

# -------------------------
# DELETE TICKET
# -------------------------
@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Ticket WHERE ticket_id = %s", (ticket_id,))
        conn.commit()
        conn.close()

        return redirect("/tickets")

    except Exception as e:
        return f"Error deleting ticket: {str(e)}"

# -------------------------
# ERROR HANDLERS
# -------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html"), 500

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)