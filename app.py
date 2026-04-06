from flask import Flask, render_template

app = Flask(__name__)

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
    tickets_data = [
        {
            "title": "Sample Ticket",
            "description": "This is a test ticket",
            "full_name": "John Doe",
            "status_label": "Open",
            "priority_level": "High"
        }
    ]
    
    return render_template("tickets.html", tickets=tickets_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)