import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- HTML ----------------

HTML_PAGE = """
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nebula</title>

<style>
body {
    margin:0;
    font-family: Arial;
    background:#0b0b0f;
    color:white;
}

/* LOGIN */
.auth {
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
}

input {
    padding:10px;
    margin:5px;
    width:200px;
    border:none;
    border-radius:8px;
}

button {
    padding:10px 15px;
    border:none;
    border-radius:8px;
    background:#7c3aed;
    color:white;
    cursor:pointer;
}

/* APP */
#app {
    display:none;
}

.nav {
    display:flex;
    justify-content:space-around;
    padding:10px;
    background:#111;
}

.post {
    background:#161622;
    margin:10px;
    padding:10px;
    border-radius:10px;
}
</style>
</head>

<body>

<!-- LOGIN -->
<div id="auth" class="auth">
    <h2>Nebula Login</h2>
    <input id="user" placeholder="username">
    <input id="pass" type="password" placeholder="password">
    <button onclick="login()">Login</button>
</div>

<!-- APP -->
<div id="app">

<div class="nav">
    <div>🏠 Home</div>
    <div>➕ Post</div>
    <div onclick="logout()">🚪 Exit</div>
</div>

<div id="feed"></div>

</div>

<script>
let posts = [
    {user:"neon", text:"Nebula ishlayapti 🚀"},
    {user:"admin", text:"Frontend ready!"}
];

function login(){
    let u = document.getElementById('user').value;
    let p = document.getElementById('pass').value;

    if(u && p){
        document.getElementById('auth').style.display="none";
        document.getElementById('app').style.display="block";
        loadFeed();
    } else {
        alert("login kiriting");
    }
}

function logout(){
    location.reload();
}

function loadFeed(){
    let feed = document.getElementById('feed');
    feed.innerHTML = "";

    posts.forEach(p=>{
        feed.innerHTML += `
        <div class="post">
            <b>@${p.user}</b>
            <p>${p.text}</p>
        </div>
        `;
    });
}
</script>

</body>
</html>
"""

# ---------------- DATABASE ----------------

users = [
    {
        "id": 1,
        "username": "neon_wolf",
        "password": "1234"
    }
]

posts = [
    {
        "id": 1,
        "userId": 1,
        "type": "image",
        "media": "https://picsum.photos/600",
        "content": "Welcome to Nebula 🚀",
        "likes": 15
    }
]

# ---------------- HOME ----------------

@app.route("/")
def home():
    return HTML_PAGE

# ---------------- LOGIN ----------------

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

# ---------------- FEED ----------------

@app.route("/feed")
def feed():
    return jsonify(posts)

# ---------------- CREATE POST ----------------

@app.route("/create-post", methods=["POST"])
def create_post():

    data = request.json

    new_post = {
        "id": len(posts) + 1,
        "userId": data.get("userId"),
        "type": data.get("type"),
        "media": data.get("media"),
        "content": data.get("content"),
        "likes": 0
    }

    posts.insert(0, new_post)

    return jsonify({
        "message": "Post created"
    })

# ---------------- LIKE ----------------

@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):

    for post in posts:

        if post["id"] == post_id:

            post["likes"] += 1

            return jsonify({
                "message": "liked"
            })

    return jsonify({
        "error": "post not found"
    })

# ---------------- START ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
