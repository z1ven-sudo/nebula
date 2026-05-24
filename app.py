import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ----------------

users = [
    {
        "id": 1,
        "username": "neon_wolf",
        "password": "1234",
        "avatar": "https://picsum.photos/seed/u1/200",
        "verified": True,
        "bio": "Cyberpunk enthusiast",
        "followers": 1250,
        "following": 340
    }
]

posts = [
    {
        "id": 1,
        "userId": 1,
        "type": "image",
        "media": "https://picsum.photos/seed/p1/600/600",
        "content": "Welcome to Nebula 🚀",
        "likes": 15,
        "comments": [],
        "timestamp": "now"
    }
]

notifications = []

# ---------------- HOME ----------------

@app.route("/")
def home():
    return jsonify({
        "app": "Nebula API",
        "status": "online"
    })

# ---------------- REGISTER ----------------

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    # CHECK USER
    for user in users:
        if user["username"] == username:
            return jsonify({
                "error": "Username already exists"
            }), 400

    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password,
        "avatar": "https://picsum.photos/200",
        "verified": False,
        "bio": "",
        "followers": 0,
        "following": 0
    }

    users.append(new_user)

    return jsonify({
        "message": "Account created",
        "user": new_user
    })

# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    for user in users:

        if user["username"] == username and user["password"] == password:

            return jsonify({
                "message": "Login success",
                "user": user
            })

    return jsonify({
        "error": "Invalid username or password"
    }), 401

# ---------------- FEED ----------------

@app.route("/feed")
def feed():
    return jsonify(posts)

# ---------------- USERS ----------------

@app.route("/users")
def get_users():
    return jsonify(users)

# ---------------- PROFILE ----------------

@app.route("/profile/<username>")
def profile(username):

    for user in users:

        if user["username"] == username:
            return jsonify(user)

    return jsonify({
        "error": "User not found"
    }), 404

# ---------------- CREATE POST ----------------

@app.route("/create-post", methods=["POST"])
def create_post():

    data = request.json

    new_post = {
        "id": len(posts) + 1,
        "userId": data.get("userId"),
        "type": data.get("type", "text"),
        "media": data.get("media", ""),
        "content": data.get("content"),
        "likes": 0,
        "comments": [],
        "timestamp": "now"
    }

    posts.insert(0, new_post)

    return jsonify({
        "message": "Post created",
        "post": new_post
    })

# ---------------- LIKE ----------------

@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):

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

# ---------------- COMMENT ----------------

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):

    data = request.json

    for post in posts:

        if post["id"] == post_id:

            new_comment = {
                "user": data.get("user"),
                "text": data.get("text")
            }

            post["comments"].append(new_comment)

            return jsonify({
                "message": "Comment added",
                "comments": post["comments"]
            })

    return jsonify({
        "error": "Post not found"
    }), 404

# ---------------- NOTIFICATIONS ----------------

@app.route("/notifications")
def get_notifications():
    return jsonify(notifications)

# ---------------- SEARCH ----------------

@app.route("/search/<query>")
def search(query):

    result = []

    for user in users:

        if query.lower() in user["username"].lower():
            result.append(user)

    return jsonify(result)



HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nebula | The Future of Social</title>
    
    <!-- External Icons (FontAwesome) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        /* --- CSS VARIABLES & THEME --- */
        :root {
            --bg-color: #050505;
            --surface-color: #0f1014;
            --surface-glass: rgba(20, 20, 25, 0.7);
            --primary-color: #8a2be2; /* BlueViolet */
            --primary-glow: rgba(138, 43, 226, 0.6);
            --accent-color: #00ffff; /* Cyan Neon */
            --accent-glow: rgba(0, 255, 255, 0.6);
            --text-main: #ffffff;
            --text-muted: #a0a0a0;
            --border-color: rgba(255, 255, 255, 0.1);
            --danger-color: #ff3b3b;
            --success-color: #00ff88;
            
            --glass-border: 1px solid rgba(255, 255, 255, 0.08);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            
            --nav-height: 60px;
            --sidebar-width: 250px;
            --header-height: 60px;
        }

        /* --- RESET & BASE --- */
        * { box-sizing: border-box; margin: 0; padding: 0; outline: none; -webkit-tap-highlight-color: transparent; }
        
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            overflow-x: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        a { text-decoration: none; color: inherit; cursor: pointer; }
        button { cursor: pointer; border: none; font-family: inherit; }
        img { display: block; max-width: 100%; object-fit: cover; }
        input, textarea { font-family: inherit; }

        /* --- UTILITY CLASSES --- */
        .glass {
            background: var(--surface-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: var(--glass-border);
            box-shadow: var(--glass-shadow);
        }
        
        .neon-text-purple { text-shadow: 0 0 10px var(--primary-glow); color: #d08aff; }
        .neon-text-cyan { text-shadow: 0 0 10px var(--accent-glow); color: #afffff; }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary-color), #6a0dad);
            color: white;
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px var(--primary-glow);
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 25px var(--primary-glow); }
        
        .btn-icon { background: transparent; color: var(--text-main); font-size: 1.2rem; padding: 8px; border-radius: 50%; transition: background 0.2s; }
        .btn-icon:hover { background: rgba(255,255,255,0.1); }
        .btn-icon.active { color: var(--primary-color); }

        .avatar { border-radius: 50%; border: 2px solid var(--border-color); }
        .avatar.online { border-color: var(--success-color); box-shadow: 0 0 8px var(--success-color); }
        
        .badge { 
            background: var(--primary-color); color: white; font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; margin-left: 4px; vertical-align: middle;
        }

        /* --- LAYOUT STRUCTURE --- */
        #app {
            display: flex;
            flex: 1;
            height: 100%;
            overflow: hidden;
            position: relative;
        }

        /* Sidebar (Desktop) */
        .sidebar {
            width: var(--sidebar-width);
            height: 100%;
            border-right: var(--glass-border);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            z-index: 100;
        }

        .logo { font-size: 1.8rem; font-weight: 700; margin-bottom: 40px; display: flex; align-items: center; gap: 10px; }
        .logo i { color: var(--accent-color); text-shadow: 0 0 10px var(--accent-glow); }

        .nav-links { display: flex; flex-direction: column; gap: 15px; }
        .nav-item { display: flex; align-items: center; gap: 15px; font-size: 1.1rem; padding: 12px; border-radius: 12px; transition: all 0.2s; color: var(--text-muted); }
        .nav-item:hover, .nav-item.active { background: rgba(255,255,255,0.05); color: var(--text-main); }
        .nav-item i { width: 24px; text-align: center; }

        /* Main Content Area */
        .main-content {
            flex: 1;
            overflow-y: auto;
            position: relative;
            scroll-behavior: smooth;
        }
        
        .feed-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Mobile Header */
        .mobile-header {
            display: none;
            height: var(--header-height);
            align-items: center;
            justify-content: space-between;
            padding: 0 15px;
            position: sticky;
            top: 0;
            z-index: 90;
            border-bottom: var(--glass-border);
        }

        /* Mobile Bottom Nav */
        .mobile-nav {
            display: none;
            height: var(--nav-height);
            border-top: var(--glass-border);
            justify-content: space-around;
            align-items: center;
            z-index: 100;
        }

        /* --- COMPONENTS --- */
        
        /* Stories */
        .stories-wrapper {
            display: flex;
            gap: 15px;
            overflow-x: auto;
            padding: 15px 0;
            margin-bottom: 20px;
            scrollbar-width: none;
        }
        .stories-wrapper::-webkit-scrollbar { display: none; }
        
        .story-circle {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 70px;
            cursor: pointer;
        }
        .ring {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            padding: 3px;
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
            margin-bottom: 5px;
        }
        .ring img { width: 100%; height: 100%; border-radius: 50%; border: 3px solid var(--bg-color); }
        .story-name { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 70px; }

        /* Post Card */
        .post {
            background: var(--surface-color);
            border-radius: 16px;
            margin-bottom: 25px;
            overflow: hidden;
            border: var(--glass-border);
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        .post-header { display: flex; align-items: center; justify-content: space-between; padding: 12px; }
        .post-user { display: flex; align-items: center; gap: 10px; }
        .post-info h4 { font-size: 0.95rem; }
        .post-info span { font-size: 0.8rem; color: var(--text-muted); display: block; }
        
        .post-media { width: 100%; background: #000; display: flex; align-items: center; justify-content: center; position: relative; }
        .post-media img, .post-media video { width: 100%; max-height: 600px; display: block; }
        
        .post-actions { padding: 12px; display: flex; justify-content: space-between; font-size: 1.4rem; }
        .action-group { display: flex; gap: 15px; }
        
        .post-content { padding: 0 12px 12px; }
        .likes-count { font-weight: 600; margin-bottom: 6px; display: block; }
        .caption { font-size: 0.95rem; margin-bottom: 6px; }
        .caption span { font-weight: 600; margin-right: 5px; color: var(--text-main); }
        .hashtags { color: var(--primary-color); font-size: 0.9rem; }
        .comments-link { color: var(--text-muted); font-size: 0.9rem; cursor: pointer; margin-top: 5px; display: block; }
        
        .comments-section {
            background: rgba(0,0,0,0.2);
            padding: 10px 12px;
            display: none;
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        .comment { font-size: 0.85rem; margin-bottom: 6px; }
        .comment strong { margin-right: 5px; }

        /* Create Post Input */
        .create-post-card {
            background: var(--surface-color);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 20px;
            border: var(--glass-border);
            display: flex;
            gap: 12px;
            align-items: center;
        }
        .create-input {
            flex: 1;
            background: rgba(255,255,255,0.05);
            border: none;
            padding: 10px 15px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
        }
        .create-input:hover { background: rgba(255,255,255,0.1); }

        /* Auth Pages */
        .auth-container {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: var(--bg-color);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: radial-gradient(circle at 50% 50%, #1a0b2e 0%, #000000 70%);
        }
        .auth-box {
            width: 100%;
            max-width: 400px;
            padding: 40px;
            text-align: center;
        }
        .auth-input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: white;
            transition: 0.3s;
        }
        .auth-input:focus { border-color: var(--primary-color); box-shadow: 0 0 10px var(--primary-glow); }
        
        /* Toast Notification */
        .toast-container {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }
        .toast {
            background: rgba(20, 20, 20, 0.95);
            border: 1px solid var(--border-color);
            padding: 10px 20px;
            border-radius: 30px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

        /* Reels / Explore Grid */
        .grid-gallery {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
        }
        .grid-item {
            position: relative;
            padding-bottom: 100%; /* Square */
            cursor: pointer;
            overflow: hidden;
        }
        .grid-item img, .grid-item video {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        .grid-item:hover img { transform: scale(1.1); }
        .grid-overlay {
            position: absolute;
            bottom: 0; left: 0; width: 100%;
            padding: 10px;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.8rem;
        }

        /* Profile Page */
        .profile-header {
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .profile-avatar-large {
            width: 100px; height: 100px;
            border-radius: 50%;
            border: 3px solid var(--primary-color);
            box-shadow: 0 0 20px var(--primary-glow);
            margin-bottom: 15px;
        }
        .profile-stats { display: flex; gap: 30px; margin: 20px 0; }
        .stat-box { display: flex; flex-direction: column; }
        .stat-num { font-weight: 700; font-size: 1.2rem; }
        .stat-label { font-size: 0.8rem; color: var(--text-muted); }
        
        .profile-actions { display: flex; gap: 10px; margin-bottom: 20px; }
        .btn-secondary { background: rgba(255,255,255,0.1); color: white; padding: 8px 20px; border-radius: 20px; font-weight: 500; }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .mobile-nav, .mobile-header { display: flex; }
            .feed-container { padding: 10px; margin-bottom: 70px; }
            .grid-gallery { gap: 1px; }
            .auth-box { padding: 20px; border: none; background: transparent; box-shadow: none; }
        }

        /* Loading Skeleton */
        .skeleton {
            background: linear-gradient(90deg, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            border-radius: 4px;
        }
        @keyframes loading { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

        /* Modal */
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 2000;
            display: none;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            width: 90%; max-width: 500px;
            padding: 20px;
            border-radius: 16px;
            position: relative;
        }
        .close-modal { position: absolute; top: 15px; right: 15px; cursor: pointer; color: var(--text-muted); }

    </style>
</head>
<body>

    <!-- --- APP CONTAINER --- -->
    <div id="app" style="display: none;">
        
        <!-- Desktop Sidebar -->
        <aside class="sidebar glass">
            <div>
                <div class="logo neon-text-purple">
                    <i class="fa-solid fa-atom"></i> Nebula
                </div>
                <nav class="nav-links">
                    <a href="#home" class="nav-item active" onclick="router.navigate('home')"><i class="fa-solid fa-house"></i> Home</a>
                    <a href="#explore" class="nav-item" onclick="router.navigate('explore')"><i class="fa-solid fa-compass"></i> Explore</a>
                    <a href="#reels" class="nav-item" onclick="router.navigate('reels')"><i class="fa-brands fa-tiktok"></i> Reels</a>
                    <a href="#messages" class="nav-item" onclick="router.navigate('messages')"><i class="fa-solid fa-paper-plane"></i> Messages</a>
                    <a href="#notifications" class="nav-item" onclick="router.navigate('notifications')"><i class="fa-solid fa-heart"></i> Notifications</a>
                    <a href="#profile" class="nav-item" onclick="router.navigate('profile')"><i class="fa-solid fa-user"></i> Profile</a>
                </nav>
            </div>
            <div class="nav-item" onclick="app.logout()"><i class="fa-solid fa-right-from-bracket"></i> Logout</div>
        </aside>

        <!-- Main Content -->
        <main class="main-content" id="main-scroll">
            <!-- Mobile Header -->
            <header class="mobile-header glass">
                <div class="logo" style="font-size: 1.5rem; margin:0;">
                    <i class="fa-solid fa-atom neon-text-cyan"></i>
                </div>
                <div style="display: flex; gap: 15px;">
                    <i class="fa-solid fa-plus-square" onclick="ui.openCreateModal()"></i>
                    <i class="fa-solid fa-bars"></i>
                </div>
            </header>

            <!-- Dynamic View Container -->
            <div id="view-container">
                <!-- Content injected via JS -->
            </div>
        </main>

        <!-- Mobile Bottom Nav -->
        <nav class="mobile-nav glass">
            <a href="#home" onclick="router.navigate('home')"><i class="fa-solid fa-house fa-lg"></i></a>
            <a href="#explore" onclick="router.navigate('explore')"><i class="fa-solid fa-compass fa-lg"></i></a>
            <a href="#reels" onclick="router.navigate('reels')"><i class="fa-brands fa-tiktok fa-lg"></i></a>
            <a href="#messages" onclick="router.navigate('messages')"><i class="fa-solid fa-paper-plane fa-lg"></i></a>
            <a href="#profile" onclick="router.navigate('profile')"><i class="fa-solid fa-user fa-lg"></i></a>
        </nav>
    </div>

    <!-- --- AUTH CONTAINER --- -->
    <div id="auth-container" class="auth-container">
        <div class="auth-box glass">
            <div class="logo neon-text-cyan" style="justify-content: center; margin-bottom: 20px;">
                <i class="fa-solid fa-atom"></i> Nebula
            </div>
            <h2 style="margin-bottom: 10px;">Welcome Back</h2>
            <p style="color: var(--text-muted); margin-bottom: 30px;">Enter the void. Connect with the galaxy.</p>
            
            <form id="auth-form" onsubmit="app.handleAuth(event)">
                <input type="text" id="username" class="auth-input" placeholder="Username / Email" required>
                <input type="password" id="password" class="auth-input" placeholder="Password" required>
                <button type="submit" class="btn-primary" style="width: 100%; margin-top: 20px;">Log In</button>
            </form>
            <p style="margin-top: 20px; font-size: 0.9rem; color: var(--text-muted);">
                Don't have an account? <a href="#" class="neon-text-purple">Sign up</a>
            </p>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <!-- Create Post Modal -->
    <div class="modal-overlay" id="create-modal">
        <div class="modal-content glass">
            <i class="fa-solid fa-xmark close-modal" onclick="ui.closeModals()"></i>
            <h3 style="margin-bottom: 15px;">Create New Post</h3>
            <textarea id="new-post-content" rows="4" class="auth-input" placeholder="What's on your mind?"></textarea>
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <button class="btn-secondary" onclick="document.getElementById('file-upload').click()"><i class="fa-solid fa-image"></i> Photo</button>
                <input type="file" id="file-upload" hidden>
            </div>
            <button class="btn-primary" style="width: 100%; margin-top: 20px;" onclick="app.createPost()">Post</button>
        </div>
    </div>

    <!-- --- JAVASCRIPT LOGIC --- -->
    <script>
        /**
         * NEBULA APP LOGIC
         * Uses a simulated Mock Backend for the single-file experience.
         */

        // --- MOCK DATABASE ---
        const db = {
            users: [
                { id: 1, username: 'neon_wolf', avatar: 'https://picsum.photos/seed/u1/200', verified: true, bio: 'Cyberpunk enthusiast. 🌌', followers: 1250, following: 340 },
                { id: 2, username: 'star_gazer', avatar: 'https://picsum.photos/seed/u2/200', verified: false, bio: 'Looking at stars.', followers: 500, following: 120 },
                { id: 3, username: 'pixel_artist', avatar: 'https://picsum.photos/seed/u3/200', verified: true, bio: 'Digital Art Creator.', followers: 8900, following: 45 },
                { id: 4, username: 'admin_nebula', avatar: 'https://picsum.photos/seed/admin/200', verified: true, role: 'admin', bio: 'System Admin', followers: 100, following: 0 }
            ],
            posts: [
                { id: 101, userId: 1, type: 'image', media: 'https://picsum.photos/seed/p1/600/600', content: 'Exploring the neon city tonight! 🌃✨ #cyberpunk #nightlife', likes: 120, comments: [{user: 'star_gazer', text: 'Awesome shot!'}], timestamp: '2h ago' },
                { id: 102, userId: 3, type: 'image', media: 'https://picsum.photos/seed/p2/600/800', content: 'New digital artwork finished. What do you think? 🎨', likes: 543, comments: [], timestamp: '5h ago' },
                { id: 103, userId: 2, type: 'video', media: 'https://picsum.photos/seed/p3/600/600', content: 'Timelapse of the galaxy 🌌', likes: 89, comments: [], timestamp: '8h ago' }
            ],
            stories: [
                { id: 1, userId: 1, img: 'https://picsum.photos/seed/s1/300', viewed: false },
                { id: 2, userId: 2, img: 'https://picsum.photos/seed/s2/300', viewed: false },
                { id: 3, userId: 3, img: 'https://picsum.photos/seed/s3/300', viewed: true },
            ],
            currentUser: null
        };

        // --- APP CONTROLLER ---
        const app = {
            init: () => {
                // Check session
                const sessionUser = localStorage.getItem('nebula_user');
                if (sessionUser) {
                    db.currentUser = JSON.parse(sessionUser);
                    app.loadApp();
                } else {
                    document.getElementById('auth-container').style.display = 'flex';
                }
            },

            handleAuth: (e) => {
                e.preventDefault();
                const userIn = document.getElementById('username').value;
                const passIn = document.getElementById('password').value;

                // Simulate Backend API Delay
                const btn = e.target.querySelector('button');
                const originalText = btn.innerText;
                btn.innerText = 'Verifying...';
                
                setTimeout(() => {
                    // Simple mock login logic
                    const user = db.users.find(u => u.username === userIn);
                    
                    if (user && passIn.length > 3) {
                        db.currentUser = user;
                        localStorage.setItem('nebula_user', JSON.stringify(user));
                        ui.toast('Welcome back to the Nebula, ' + user.username);
                        document.getElementById('auth-container').style.display = 'none';
                        app.loadApp();
                    } else {
                        ui.toast('Invalid credentials. Try "neon_wolf" / "1234"', 'error');
                    }
                    btn.innerText = originalText;
                }, 1000);
            },

            logout: () => {
                localStorage.removeItem('nebula_user');
                location.reload();
            },

            loadApp: () => {
                document.getElementById('app').style.display = 'flex';
                router.navigate('home');
            },

            createPost: () => {
                const content = document.getElementById('new-post-content').value;
                if(!content) return;

                // Add to simulated DB
                const newPost = {
                    id: Date.now(),
                    userId: db.currentUser.id,
                    type: 'text',
                    content: content,
                    likes: 0,
                    comments: [],
                    timestamp: 'Just now'
                };
                db.posts.unshift(newPost);
                
                ui.closeModals();
                ui.toast('Post created successfully!');
                document.getElementById('new-post-content').value = '';
                
                // Refresh feed if on home
                if(router.current === 'home') router.renderHome();
            },

            toggleLike: (id, btn) => {
                btn.classList.toggle('active');
                // Find post and update mock DB
                const post = db.posts.find(p => p.id === id);
                if(post) {
                    post.likes += btn.classList.contains('active') ? 1 : -1;
                    // Update UI counter
                    const counter = btn.closest('.post').querySelector('.likes-count');
                    counter.innerText = post.likes + ' likes';
                }
            }
        };

        // --- ROUTER & VIEWS ---
        const router = {
            current: 'home',
            
            navigate: (route) => {
                router.current = route;
                const container = document.getElementById('view-container');
                const main = document.getElementById('main-scroll');
                
                // Update active nav
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                const activeLink = document.querySelector(`a[href="#${route}"]`);
                if(activeLink) activeLink.classList.add('active');

                main.scrollTop = 0;

                // Render Skeleton first
                container.innerHTML = `<div class="feed-container"><div class="skeleton" style="height: 300px; margin-bottom:20px;"></div><div class="skeleton" style="height: 300px;"></div></div>`;

                // Simulate Route Loading Delay
                setTimeout(() => {
                    if (route === 'home') router.renderHome();
                    else if (route === 'explore') router.renderExplore();
                    else if (route === 'reels') router.renderReels();
                    else if (route === 'profile') router.renderProfile();
                    else if (route === 'messages') router.renderMessages();
                    else if (route === 'notifications') router.renderNotifications();
                }, 400);
            },

            renderHome: () => {
                const container = document.getElementById('view-container');
                
                // Render Stories
                let storiesHtml = `<div class="stories-wrapper">`;
                // Add "My Story"
                storiesHtml += `
                    <div class="story-circle">
                        <div class="ring" style="border: 2px dashed var(--text-muted); background: none; display:flex; align-items:center; justify-content:center;">
                            <i class="fa-solid fa-plus" style="font-size: 1.5rem; color:white;"></i>
                        </div>
                        <span class="story-name">Add Story</span>
                    </div>`;
                
                db.stories.forEach(s => {
                    const user = db.users.find(u => u.id === s.userId);
                    storiesHtml += `
                        <div class="story-circle" onclick="ui.viewStory(${s.id})">
                            <div class="ring" style="background: ${s.viewed ? '#333' : 'linear-gradient(45deg, var(--primary-color), var(--accent-color))'}">
                                <img src="${user.avatar}" alt="${user.username}">
                            </div>
                            <span class="story-name">${user.username}</span>
                        </div>`;
                });
                storiesHtml += `</div>`;

                // Render Posts
                let postsHtml = `<div class="feed-container">
                    <div class="create-post-card">
                        <img src="${db.currentUser.avatar}" class="avatar" width="40" height="40">
                        <input type="text" class="create-input" placeholder="Start a thread..." readonly onclick="ui.openCreateModal()">
                    </div>
                    ${storiesHtml}
                `;

                db.posts.forEach(post => {
                    const user = db.users.find(u => u.id === post.userId);
                    const verifiedBadge = user.verified ? `<i class="fa-solid fa-circle-check badge" style="color: var(--accent-color); background:none;"></i>` : '';
                    
                    let mediaHtml = '';
                    if(post.type === 'image') {
                        mediaHtml = `<img src="${post.media}" alt="Post Content">`;
                    } else if(post.type === 'video') {
                        mediaHtml = `<video src="${post.media}" controls poster="${post.media}"></video>`;
                    }

                    // Comments Preview
                    let commentsHtml = '';
                    post.comments.slice(0, 2).forEach(c => {
                        commentsHtml += `<div class="comment"><strong>${c.user}</strong> ${c.text}</div>`;
                    });

                    postsHtml += `
                        <article class="post glass">
                            <div class="post-header">
                                <div class="post-user">
                                    <img src="${user.avatar}" class="avatar" width="35" height="35">
                                    <div class="post-info">
                                        <h4>${user.username} ${verifiedBadge}</h4>
                                        <span>${post.timestamp}</span>
                                    </div>
                                </div>
                                <i class="fa-solid fa-ellipsis btn-icon"></i>
                            </div>
                            <div class="post-media">
                                ${mediaHtml}
                            </div>
                            <div class="post-actions">
                                <div class="action-group">
                                    <button class="btn-icon" onclick="app.toggleLike(${post.id}, this)"><i class="fa-regular fa-heart"></i></button>
                                    <button class="btn-icon"><i class="fa-regular fa-comment"></i></button>
                                    <button class="btn-icon"><i class="fa-regular fa-paper-plane"></i></button>
                                </div>
                                <button class="btn-icon"><i class="fa-regular fa-bookmark"></i></button>
                            </div>
                            <div class="post-content">
                                <span class="likes-count">${post.likes} likes</span>
                                <div class="caption">
                                    <span>${user.username}</span> ${post.content}
                                </div>
                                ${post.comments.length > 0 ? `<div class="comments-section" style="display:block">${commentsHtml}</div>` : ''}
                                <span class="comments-link" onclick="ui.toast('Comments full view coming soon')">View all ${post.comments.length} comments</span>
                            </div>
                        </article>
                    `;
                });
                postsHtml += `</div>`; // End container

                container.innerHTML = postsHtml;
            },

            renderExplore: () => {
                const container = document.getElementById('view-container');
                let html = `<div class="feed-container"><h2 style="margin-bottom:15px;">Explore</h2><div class="grid-gallery">`;
                
                // Generate dummy grid items
                for(let i=0; i<15; i++) {
                    html += `
                        <div class="grid-item">
                            <img src="https://picsum.photos/seed/explore${i}/400/400">
                            <div class="grid-overlay">
                                <i class="fa-solid fa-heart"></i> ${Math.floor(Math.random()*500)}
                                <i class="fa-solid fa-comment" style="margin-left:10px"></i> ${Math.floor(Math.random()*50)}
                            </div>
                        </div>
                    `;
                }
                html += `</div></div>`;
                container.innerHTML = html;
            },

            renderReels: () => {
                const container = document.getElementById('view-container');
                container.innerHTML = `
                    <div style="height: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; color: var(--text-muted);">
                        <i class="fa-brands fa-tiktok" style="font-size: 4rem; margin-bottom: 20px; color: var(--primary-color);"></i>
                        <h2>Reels</h2>
                        <p>Vertical short video feed</p>
                        <div style="margin-top: 20px; width: 300px; height: 500px; background: #111; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px dashed #333;">
                            Video Player Simulation
                        </div>
                    </div>
                `;
            },

            renderProfile: () => {
                const u = db.currentUser;
                const container = document.getElementById('view-container');
                
                // Generate user grid
                let gridHtml = `<div class="grid-gallery" style="max-width:600px; margin:0 auto;">`;
                db.posts.filter(p => p.userId === u.id).forEach(p => {
                     gridHtml += `<div class="grid-item"><img src="${p.media || 'https://picsum.photos/seed/'+p.id+'/400'}"></div>`;
                });
                gridHtml += `</div>`;

                container.innerHTML = `
                    <div class="glass" style="min-height: 100%; padding-bottom: 50px;">
                        <div class="profile-header">
                            <img src="${u.avatar}" class="profile-avatar-large">
                            <h2>${u.username} ${u.verified ? '<i class="fa-solid fa-circle-check badge" style="background:none; color:var(--accent-color)"></i>' : ''}</h2>
                            <p style="color:var(--text-muted); margin-top: 5px;">${u.bio}</p>
                            
                            <div class="profile-stats">
                                <div class="stat-box"><span class="stat-num">${db.posts.filter(p => p.userId === u.id).length}</span><span class="stat-label">Posts</span></div>
                                <div class="stat-box"><span class="stat-num">${u.followers}</span><span class="stat-label">Followers</span></div>
                                <div class="stat-box"><span class="stat-num">${u.following}</span><span class="stat-label">Following</span></div>
                            </div>

                            <div class="profile-actions">
                                <button class="btn-secondary">Edit Profile</button>
                                <button class="btn-secondary"><i class="fa-solid fa-share"></i></button>
                            </div>
                        </div>
                        
                        <!-- Tabs -->
                        <div style="display:flex; border-bottom: 1px solid var(--border-color); margin-top: 10px;">
                            <div style="flex:1; text-align:center; padding:15px; border-bottom: 2px solid white;"><i class="fa-solid fa-grid"></i></div>
                            <div style="flex:1; text-align:center; padding:15px; color:var(--text-muted);"><i class="fa-solid fa-bookmark"></i></div>
                            <div style="flex:1; text-align:center; padding:15px; color:var(--text-muted);"><i class="fa-solid fa-user-lock"></i></div>
                        </div>

                        ${gridHtml}
                    </div>
                `;
            },

            renderMessages: () => {
                const container = document.getElementById('view-container');
                container.innerHTML = `
                    <div class="feed-container">
                        <h2 style="margin-bottom:20px;">Messages</h2>
                        <div class="create-post-card" style="margin-bottom: 0;">
                            <i class="fa-solid fa-magnifying-glass" style="color:var(--text-muted)"></i>
                            <input type="text" class="create-input" placeholder="Search users" style="background:transparent;">
                        </div>
                        
                        <div style="margin-top: 20px;">
                            ${[1,2,3].map(id => {
                                const u = db.users.find(user => user.id === id);
                                return `
                                <div style="display:flex; align-items:center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                                    <div style="position:relative">
                                        <img src="${u.avatar}" class="avatar" width="50" height="50">
                                        <div style="position:absolute; bottom:2px; right:2px; width:12px; height:12px; background:var(--success-color); border-radius:50%; border:2px solid var(--bg-color);"></div>
                                    </div>
                                    <div style="margin-left: 15px; flex:1;">
                                        <div style="display:flex; justify-content:space-between;">
                                            <h4 style="font-size: 1rem;">${u.username}</h4>
                                            <span style="font-size:0.7rem; color:var(--text-muted);">2m</span>
                                        </div>
                                        <p style="font-size:0.9rem; color:var(--text-muted); margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width: 200px;">Hey! Are you going to the event?</p>
                                    </div>
                                </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            },

            renderNotifications: () => {
                 const container = document.getElementById('view-container');
                 container.innerHTML = `
                    <div class="feed-container">
                        <h2 style="margin-bottom:20px;">Notifications</h2>
                        <div style="margin-bottom: 20px;">
                            <span style="font-size:0.9rem; color:var(--text-muted); font-weight:600; text-transform:uppercase;">Today</span>
                            <div style="display:flex; align-items:center; padding: 15px 10px;">
                                <div style="width:40px; height:40px; background:var(--primary-color); border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                                    <i class="fa-solid fa-heart"></i>
                                </div>
                                <p><strong>neon_wolf</strong> liked your photo.</p>
                            </div>
                            <div style="display:flex; align-items:center; padding: 15px 10px;">
                                <img src="${db.users[1].avatar}" class="avatar" width="40" height="40" style="margin-right:15px;">
                                <p><strong>star_gazer</strong> started following you.</p>
                                <button class="btn-primary" style="padding: 5px 15px; font-size: 0.8rem; margin-left: auto;">Follow</button>
                            </div>
                        </div>
                    </div>
                 `;
            }
        };

        // --- UI HELPERS ---
        const ui = {
            toast: (msg, type = 'success') => {
                const container = document.getElementById('toast-container');
                const el = document.createElement('div');
                el.className = 'toast glass';
                const icon = type === 'success' ? '<i class="fa-solid fa-check-circle" style="color:var(--success-color)"></i>' : '<i class="fa-solid fa-exclamation-circle" style="color:var(--danger-color)"></i>';
                el.innerHTML = `${icon} <span>${msg}</span>`;
                container.appendChild(el);
                setTimeout(() => {
                    el.style.opacity = '0';
                    el.style.transform = 'translateY(20px)';
                    setTimeout(() => el.remove(), 300);
                }, 3000);
            },

            openCreateModal: () => {
                document.getElementById('create-modal').style.display = 'flex';
            },

            closeModals: () => {
                document.querySelectorAll('.modal-overlay').forEach(el => el.style.display = 'none');
            },

            viewStory: (id) => {
                const s = db.stories.find(x => x.id === id);
                const user = db.users.find(u => u.id === s.userId);
                
                // Full screen story simulation
                const overlay = document.createElement('div');
                overlay.className = 'modal-overlay';
                overlay.style.display = 'flex';
                overlay.style.zIndex = '3000';
                overlay.innerHTML = `
                    <div style="width:100%; max-width:400px; height: 80vh; position:relative; border-radius:10px; overflow:hidden; background: #000;">
                        <img src="${s.img}" style="width:100%; height:100%; object-fit:cover;">
                        <div style="position:absolute; top:20px; left:20px; display:flex; align-items:center; width:100%;">
                            <img src="${user.avatar}" class="avatar" width="35" height="35">
                            <span style="margin-left:10px; font-weight:600; text-shadow: 0 1px 3px rgba(0,0,0,0.8);">${user.username}</span>
                            <i class="fa-solid fa-xmark" style="margin-left:auto; font-size:1.5rem; cursor:pointer;" onclick="this.closest('.modal-overlay').remove()"></i>
                        </div>
                        <!-- Progress Bar -->
                        <div style="position:absolute; top:10px; left:10px; right:10px; height:2px; background:rgba(255,255,255,0.3); border-radius:2px;">
                            <div style="width:100%; height:100%; background:white; animation: storyProgress 5s linear forwards;"></div>
                        </div>
                        <style>@keyframes storyProgress { from {width:0%} to {width:100%} }</style>
                    </div>
                `;
                document.body.appendChild(overlay);

                // Auto close
                setTimeout(() => {
                    if(overlay.parentNode) overlay.remove();
                }, 5000);
            }
        };

        // --- INIT ---
        window.addEventListener('load', app.init);

        // Handle browser back button
        window.addEventListener('popstate', () => {
            // Simple hash handling
            const hash = location.hash.replace('#', '') || 'home';
            router.navigate(hash);
        });

    </script>
</body>
</html> 


"""


# ---------------- START ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
