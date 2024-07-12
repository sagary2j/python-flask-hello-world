from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import datetime as dt
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Initialize database
try:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, date_of_birth DATE)")
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")

@app.route("/hello/<username>", methods=["PUT"])
def save_user_data(username):
    data = request.get_json()
    date_of_birth = data["dateOfBirth"]
    
    if not username.isalpha():
        return jsonify({"error": "Username must contain only letters"}), 400
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if datetime.strptime(date_of_birth, "%Y-%m-%d") >= datetime.today():
        return jsonify({"error": "Date of birth must be in the past."}), 400
    
    conn = sqlite3.connect("users.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO users (username, date_of_birth) VALUES (?, ?)", (username, date_of_birth))
        conn.commit()
        #conn.close()
        return "", 204
    except (Exception, sqlite3.Error) as error:
        print("Error updating user:", error)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()  # Close connection even on

@app.route("/hello/<username>", methods=["GET"])
def get_hello_message(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date_of_birth FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        date_of_birth = datetime.strptime(result[0], "%Y-%m-%d")
        today = datetime.today()
        this_year_birthday = datetime(today.year, date_of_birth.month, date_of_birth.day)
        if today > this_year_birthday:
            next_year_birthday = datetime(today.year + 1, date_of_birth.month, date_of_birth.day)
            delta = next_year_birthday - today
        else:
            delta = this_year_birthday - today
        days_until_birthday = delta.days + 1
        if days_until_birthday == 365:  # Check if today is the birthday
            message = f"Hello, {username}! Happy birthday!"
        else:
            message = f"Hello, {username}! Your birthday is in {days_until_birthday} day(s)"
    else:
        message = f"User {username} not found"
    conn.close()
    return jsonify({"message": message}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy Application", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

