import os
from flask import Flask, jsonify, request

app = Flask(__name__)

users = []

# Home
@app.route("/")
def home():
    return jsonify({
        "status": "Nebula online"
    })

# Register
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    # check
    for user in users:
        if user["username"] == username:
            return jsonify({
                "error": "Username already exists"
            }), 400

    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password
    }

    users.append(new_user)

    return jsonify({
        "message": "Account created",
        "user": username
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
                "message": "Login success",
                "username": username
            })

    return jsonify({
        "error": "Invalid username or password"
    }), 401

# Users
@app.route("/users")
def get_users():
    return jsonify(users)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
