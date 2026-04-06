import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

conn = mysql.connector.connect(
    host="44.193.107.126",
    user="root",
    password="password",
    database="helpdesk"
)

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
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT t.ticket_id, t.title, u.full_name, s.status_label, p.priority_level
    FROM Ticket t
    JOIN User u ON t.user_id = u.user_id
    JOIN Status s ON t.status_id = s.status_id
    JOIN Priority p ON t.priority_id = p.priority_id
    """)

    data = cursor.fetchall()
    return str(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)