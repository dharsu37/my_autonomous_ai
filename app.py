from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def log_message(msg):
    conn = sqlite3.connect("assistant.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (message) VALUES (?)", (msg,))
    conn.commit()
    conn.close()

# Dummy AI logic with multi-task handling
def process_message(msg):
    msg_lower = msg.lower()
    if "meeting" in msg_lower:
        return "Meeting noted! ✅", {"type":"meeting"}
    elif "order" in msg_lower or "food" in msg_lower:
        return "How many servings?", {"type":"order"}
    elif "food ready" in msg_lower:
        return "Checking ingredients… 🍲", {"type":"food"}
    else:
        return f"Unknown command: {msg}", {"type":"unknown"}

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Send message
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    msg = data.get("message", "")
    log_message(msg)  # Log to SQLite

    # For multi-task: split by commas
    tasks = [t.strip() for t in msg.split(",")]
    responses = []
    results = []
    for task in tasks:
        resp, res = process_message(task)
        responses.append(resp)
        results.append(res)

    return jsonify({"responses": responses, "result": results})

# Status tracking endpoint (dummy example)
@app.route("/status")
def status():
    # Example status dictionary
    status_dict = {
        "Meeting": "Completed ✅",
        "Order": "Pending 🍴",
        "Food": "Cooking 🔥"
    }
    return jsonify(status_dict)

if __name__ == "__main__":
    app.run(debug=True)