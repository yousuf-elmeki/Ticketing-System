import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

# Config details
db_config = {
    "host": "44.193.107.126",
    "user": "root",
    "password": "password",
    "database": "helpdesk"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

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
    # 1. Connect to the DB
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 2. Execute the join query
    cursor.execute("""
        SELECT t.ticket_id, t.title, t.description, u.full_name, 
               s.status_label, p.priority_level
        FROM Ticket t
        JOIN User u ON t.user_id = u.user_id
        JOIN Status s ON t.status_id = s.status_id
        JOIN Priority p ON t.priority_id = p.priority_id
    """)

    tickets_data = cursor.fetchall()
    
    # 3. Close the "worker" and the connection
    cursor.close()
    db.close()

    return render_template("tickets.html", tickets=tickets_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)