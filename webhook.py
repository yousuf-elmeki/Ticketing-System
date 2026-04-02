from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/update", methods=["POST"])
def update():
    os.system("cd /home/ubuntu/Database-Final-Project && git pull")
    os.system("pkill -f app.py")
    os.system("nohup python3 /home/ubuntu/Database-Final-Project/app.py &")
    return "Updated", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)