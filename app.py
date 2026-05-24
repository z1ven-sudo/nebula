import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake database
users = [
    {
        "id": 1,
        "username": "riza",
        "bio": "Nebula CEO",
        "followers": 1200
    }
]

posts = [
    {
        "id": 1,
        "user": "riza",
        "caption": "Welcome to Nebula",
        "likes": 15,
        "comments": []
    }
]

# Home
@app.route("/")
def home():
    return jsonify({
        "app": "Nebula API",
        "status": "online"
    })

# Register
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "bio": "",
        "followers": 0
    }

    users.append(new_user)

    return jsonify({
        "message": "User created",
        "user": new_user
    })

# Login
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    return jsonify({
        "message": "Login success",
        "username": data["username"]
    })

# All users
@app.route("/users")
def get_users():
    return jsonify(users)

# Single profile
@app.route("/profile/<username>")
def profile(username):

    for user in users:
        if user["username"] == username:
            return jsonify(user)

    return jsonify({
        "error": "User not found"
    }), 404

# Create post
@app.route("/create-post", methods=["POST"])
def create_post():

    data = request.json

    new_post = {
        "id": len(posts) + 1,
        "user": data["user"],
        "caption": data["caption"],
        "likes": 0,
        "comments": []
    }

    posts.append(new_post)

    return jsonify({
        "message": "Post created",
        "post": new_post
    })

# Feed
@app.route("/feed")
def feed():
    return jsonify(posts)

# Like post
@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):

    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1

            return jsonify({
                "message": "Post liked",
                "likes": post["likes"]
            })

    return jsonify({
        "error": "Post not found"
    }), 404

# Comment
@app.route("/comment/<int:post_id>", methods=["POST"])
def comment_post(post_id):

    data = request.json

    for post in posts:
        if post["id"] == post_id:

            post["comments"].append({
                "user": data["user"],
                "text": data["text"]
            })

            return jsonify({
                "message": "Comment added",
                "comments": post["comments"]
            })

    return jsonify({
        "error": "Post not found"
    }), 404

# Start server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
