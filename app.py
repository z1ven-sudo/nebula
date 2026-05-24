import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

users = []

# Frontend
@app.route("/")
def home():
    return render_template("index.html")

# Register
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username:
            return jsonify({
                "error": "Username already exists"
            }), 400

    users.append({
        "username": username,
        "password": password
    })

    return jsonify({
        "message": "Account created"
    })

# Login
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:

            return jsonify({
                "message": "Login success"
            })

    return jsonify({
        "error": "Invalid login"
    }), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
