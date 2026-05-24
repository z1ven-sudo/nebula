import os
import random
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
#             DATABASE (IN-MEMORY)
# ==========================================

users = [
    {"id": 1, "username": "neon_user", "password": "123", "avatar": "https://i.pravatar.cc/150?u=1", "bio": "Living in the grid.", "followers": 1200, "following": 450},
    {"id": 2, "username": "cyber_punk", "password": "123", "avatar": "https://i.pravatar.cc/150?u=2", "bio": "Glitch enthusiast.", "followers": 850, "following": 200},
    {"id": 3, "username": "star_gazer", "password": "123", "avatar": "https://i.pravatar.cc/150?u=3", "bio": "Exploring the nebula.", "followers": 3400, "following": 120}
]

posts = [
    {
        "id": 1, "userId": 2, "username": "cyber_punk", "avatar": "https://i.pravatar.cc/150?u=2",
        "type": "image", "media": "https://picsum.photos/600/600?random=1", 
        "content": "Night city vibes 🌃✨ #cyberpunk", "likes": 42, "comments": []
    },
    {
        "id": 2, "userId": 3, "username": "star_gazer", "avatar": "https://i.pravatar.cc/150?u=3",
        "type": "image", "media": "https://picsum.photos/600/800?random=2", 
        "content": "Lost in space 🚀", "likes": 128, "comments": [{"user": "neon_user", "text": "Amazing view!"}]
    }
]

stories = [
    {"userId": 2, "username": "cyber_punk", "avatar": "https://i.pravatar.cc/150?u=2"},
    {"userId": 3, "username": "star_gazer", "avatar": "https://i.pravatar.cc/150?u=3"},
    {"userId": 1, "username": "neon_user", "avatar": "https://i.pravatar.cc/150?u=1"} # Self story placeholder
]

# ==========================================
#               FRONTEND
# ==========================================

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEBULA | Next-Gen Social</title>
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <!-- Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-dark: #050510;
            --bg-panel: rgba(20, 20, 35, 0.6);
            --primary: #00f3ff; /* Neon Cyan */
            --secondary: #bc13fe; /* Neon Purple */
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
            --glass-border: 1px solid rgba(255, 255, 255, 0.1);
            --neon-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            --purple-shadow: 0 0 10px rgba(188, 19, 254, 0.5);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Rajdhani', sans-serif;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(188, 19, 254, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 243, 255, 0.1) 0%, transparent 20%);
            min-height: 100vh;
        }

        /* UTILITIES */
        .glass {
            background: var(--bg-panel);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: var(--glass-border);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }

        .neon-text { color: var(--primary); text-shadow: 0 0 5px var(--primary); }
        .purple-text { color: var(--secondary); text-shadow: 0 0 5px var(--secondary); }
        .hidden { display: none !important; }
        .btn {
            cursor: pointer; border: none; outline: none; font-family: 'Orbitron', sans-serif;
            transition: all 0.3s ease;
        }

        /* AUTH SCREEN */
        #auth-screen {
            height: 100vh; display: flex; align-items: center; justify-content: center;
            background: radial-gradient(circle, rgba(20,20,40,0.8) 0%, #050510 100%);
        }
        .auth-card { width: 100%; max-width: 400px; padding: 40px; text-align: center; }
        .logo-title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; margin-bottom: 30px; letter-spacing: 2px; }
        .input-group { margin-bottom: 20px; text-align: left; }
        .input-group label { display: block; margin-bottom: 8px; color: var(--primary); font-size: 0.9rem; }
        input {
            width: 100%; padding: 12px; background: rgba(0,0,0,0.3); border: 1px solid #333;
            color: white; border-radius: 8px; font-family: 'Rajdhani', sans-serif; font-size: 1.1rem;
        }
        input:focus { border-color: var(--primary); box-shadow: var(--neon-shadow); outline: none; }
        .action-btn {
            width: 100%; padding: 12px; background: linear-gradient(90deg, var(--secondary), #8a2be2);
            color: white; font-weight: bold; font-size: 1.1rem; border-radius: 8px; margin-top: 10px;
        }
        .action-btn:hover { box-shadow: var(--purple-shadow); transform: translateY(-2px); }
        .switch-auth { margin-top: 20px; font-size: 0.9rem; color: var(--text-muted); cursor: pointer; }
        .switch-auth:hover { color: var(--primary); }

        /* MAIN APP LAYOUT */
        #app-screen { display: flex; max-width: 1200px; margin: 0 auto; min-height: 100vh; }
        
        /* SIDEBAR (Desktop) */
        .sidebar {
            width: 250px; padding: 20px; border-right: var(--glass-border);
            position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column;
        }
        .nav-item {
            display: flex; align-items: center; gap: 15px; padding: 15px;
            color: var(--text-muted); font-size: 1.2rem; cursor: pointer; border-radius: 10px; margin-bottom: 5px;
        }
        .nav-item:hover, .nav-item.active { background: rgba(255,255,255,0.05); color: var(--primary); }
        .nav-item i { width: 25px; text-align: center; }

        /* MAIN FEED */
        .main-content { flex: 1; padding: 20px; max-width: 600px; margin: 0 auto; border-left: var(--glass-border); border-right: var(--glass-border); }
        
        /* STORIES */
        .stories-container { display: flex; gap: 15px; overflow-x: auto; padding-bottom: 15px; margin-bottom: 20px; scrollbar-width: none; }
        .stories-container::-webkit-scrollbar { display: none; }
        .story-item { display: flex; flex-direction: column; align-items: center; cursor: pointer; min-width: 70px; }
        .story-ring {
            width: 64px; height: 64px; border-radius: 50%;
            padding: 3px; background: linear-gradient(45deg, var(--secondary), var(--primary));
            margin-bottom: 5px; position: relative;
        }
        .story-ring img { width: 100%; height: 100%; border-radius: 50%; border: 3px solid var(--bg-dark); object-fit: cover; }
        .story-username { font-size: 0.75rem; color: var(--text-muted); }

        /* POST CARD */
        .post-card { margin-bottom: 30px; overflow: hidden; animation: fadeIn 0.5s ease; }
        .post-header { display: flex; align-items: center; padding: 15px; gap: 12px; }
        .user-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 1px solid var(--primary); }
        .username { font-weight: bold; color: var(--text-main); }
        .post-media { width: 100%; display: block; max-height: 600px; object-fit: cover; background: #000; }
        .post-actions { padding: 10px 15px; display: flex; gap: 20px; font-size: 1.5rem; }
        .action-icon { cursor: pointer; transition: transform 0.2s; }
        .action-icon:hover { color: var(--primary); transform: scale(1.1); }
        .action-icon.liked { color: #ff0055; text-shadow: 0 0 10px #ff0055; }
        .post-content { padding: 0 15px 15px; font-size: 0.95rem; line-height: 1.4; }
        .likes-count { font-weight: bold; margin-bottom: 5px; display: block; }
        
        /* CREATE POST */
        .create-post { padding: 15px; margin-bottom: 20px; display: flex; gap: 10px; align-items: center; }
        .create-input { flex: 1; background: transparent; border: none; color: white; font-size: 1rem; }
        .create-input:focus { box-shadow: none; border: none; }

        /* EXPLORE GRID */
        .grid-gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .grid-item { aspect-ratio: 1; position: relative; cursor: pointer; overflow: hidden; border-radius: 8px; }
        .grid-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
        .grid-item:hover img { transform: scale(1.1); }
        .grid-overlay {
            position: absolute; inset: 0; background: rgba(0,0,0,0.5); display: flex;
            justify-content: center; align-items: center; gap: 15px; opacity: 0; transition: opacity 0.3s;
        }
        .grid-item:hover .grid-overlay { opacity: 1; }

        /* PROFILE */
        .profile-header { text-align: center; padding: 30px 20px; margin-bottom: 20px; position: relative; overflow: hidden; }
        .profile-header::before {
            content: ''; position: absolute; top: -50px; left: 50%; transform: translateX(-50%);
            width: 200px; height: 200px; background: var(--secondary); filter: blur(80px); z-index: -1; opacity: 0.5;
        }
        .profile-pic-lg { width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--primary); margin-bottom: 15px; object-fit: cover; }
        .profile-stats { display: flex; justify-content: center; gap: 30px; margin: 20px 0; }
        .stat-box { text-align: center; }
        .stat-num { display: block; font-weight: bold; font-size: 1.2rem; }
        .stat-label { font-size: 0.8rem; color: var(--text-muted); }
        .bio { color: var(--text-muted); max-width: 80%; margin: 0 auto; }

        /* BOTTOM NAV (Mobile) */
        .mobile-nav {
            display: none; position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(5, 5, 16, 0.95); backdrop-filter: blur(10px);
            border-top: var(--glass-border); padding: 15px; justify-content: space-around; z-index: 100;
        }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .mobile-nav { display: flex; }
            .main-content { border: none; margin-bottom: 60px; padding: 10px; }
            #app-screen { display: block; }
        }
    </style>
</head>
<body>

    <!-- AUTH SCREEN -->
    <div id="auth-screen">
        <div class="glass auth-card">
            <h1 class="logo-title"><span class="neon-text">NEBULA</span></h1>
            
            <!-- Login Form -->
            <form id="login-form">
                <div class="input-group">
                    <label>USERNAME</label>
                    <input type="text" id="login-username" placeholder="Enter username" required>
                </div>
                <div class="input-group">
                    <label>PASSWORD</label>
                    <input type="password" id="login-password" placeholder="••••••" required>
                </div>
                <button type="submit" class="btn action-btn">ENTER THE GRID</button>
            </form>

            <!-- Register Form (Hidden) -->
            <form id="register-form" class="hidden">
                <div class="input-group">
                    <label>CHOOSE USERNAME</label>
                    <input type="text" id="reg-username" placeholder="Create username" required>
                </div>
                <div class="input-group">
                    <label>SET PASSWORD</label>
                    <input type="password" id="reg-password" placeholder="••••••" required>
                </div>
                <button type="submit" class="btn action-btn" style="background: linear-gradient(90deg, var(--primary), #0088ff); INITIALIZE ID">INITIALIZE ID</button>
            </form>

            <div class="switch-auth" onclick="toggleAuth()">Don't have an ID? <span class="neon-text">Register</span></div>
        </div>
    </div>

    <!-- APP SCREEN -->
    <div id="app-screen" class="hidden">
        
        <!-- Desktop Sidebar -->
        <div class="glass sidebar">
            <h1 class="logo-title" style="font-size: 1.8rem; margin-bottom: 40px;"><span class="neon-text">NEBULA</span></h1>
            <div class="nav-item active" onclick="navTo('feed')"><i class="fa-solid fa-house"></i> Feed</div>
            <div class="nav-item" onclick="navTo('explore')"><i class="fa-solid fa-compass"></i> Explore</div>
            <div class="nav-item" onclick="navTo('notifications')"><i class="fa-solid fa-bell"></i> Alerts</div>
            <div class="nav-item" onclick="navTo('profile')"><i class="fa-solid fa-user"></i> Profile</div>
            <div style="margin-top: auto;">
                <div class="nav-item" onclick="logout()"><i class="fa-solid fa-power-off" style="color: #ff4444;"></i> Logout</div>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="main-content">
            
            <!-- Feed View -->
            <div id="view-feed">
                <!-- Stories -->
                <div class="stories-container" id="stories-wrapper">
                    <!-- Stories injected via JS -->
                </div>

                <!-- Create Post -->
                <div class="glass create-post">
                    <img id="current-user-avatar" src="" class="user-avatar" style="width:35px; height:35px;">
                    <input type="text" id="new-post-content" class="create-input" placeholder="Broadcast your thoughts...">
                    <button class="btn" style="color:var(--primary)" onclick="createPost()"><i class="fa-solid fa-paper-plane"></i></button>
                </div>

                <!-- Posts -->
                <div id="feed-container">
                    <!-- Posts injected via JS -->
                </div>
            </div>

            <!-- Explore View -->
            <div id="view-explore" class="hidden">
                <h2 class="neon-text" style="margin-bottom: 20px;">EXPLORE THE GRID</h2>
                <div class="grid-gallery" id="explore-grid">
                    <!-- Grid items injected JS -->
                </div>
            </div>

            <!-- Notifications View (UI Only) -->
            <div id="view-notifications" class="hidden">
                <h2 class="neon-text" style="margin-bottom: 20px;">SYSTEM ALERTS</h2>
                <div class="glass" style="padding: 15px; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                    <div style="background: var(--secondary); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"><i class="fa-solid fa-heart"></i></div>
                    <div><strong>cyber_punk</strong> liked your post.<br><small style="color: var(--text-muted)">2 mins ago</small></div>
                </div>
                <div class="glass" style="padding: 15px; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                    <div style="background: var(--primary); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: black;"><i class="fa-solid fa-user-plus"></i></div>
                    <div><strong>star_gazer</strong> started following you.<br><small style="color: var(--text-muted)">1 hour ago</small></div>
                </div>
            </div>

            <!-- Profile View -->
            <div id="view-profile" class="hidden">
                <div class="glass profile-header">
                    <img id="profile-img" src="" class="profile-pic-lg">
                    <h2 id="profile-name" style="margin-bottom: 5px;">Username</h2>
                    <p id="profile-bio" class="bio">Bio goes here...</p>
                    
                    <div class="profile-stats">
                        <div class="stat-box"><span class="stat-num" id="profile-posts">0</span><span class="stat-label">Posts</span></div>
                        <div class="stat-box"><span class="stat-num" id="profile-followers">0</span><span class="stat-label">Followers</span></div>
                        <div class="stat-box"><span class="stat-num" id="profile-following">0</span><span class="stat-label">Following</span></div>
                    </div>
                    
                    <button class="btn action-btn" style="padding: 8px 20px; font-size: 0.9rem;">EDIT PROFILE</button>
                </div>
                <div class="grid-gallery" id="profile-grid">
                    <!-- User posts -->
                </div>
            </div>

        </div>
    </div>

    <!-- Mobile Bottom Nav -->
    <div class="glass mobile-nav">
        <div class="nav-item active" onclick="navTo('feed')"><i class="fa-solid fa-house"></i></div>
        <div class="nav-item" onclick="navTo('explore')"><i class="fa-solid fa-compass"></i></div>
        <div class="nav-item" onclick="navTo('notifications')"><i class="fa-solid fa-bell"></i></div>
        <div class="nav-item" onclick="navTo('profile')"><i class="fa-solid fa-user"></i></div>
    </div>

    <script>
        // --- STATE & CONFIG ---
        const API_URL = ""; 
        let currentUser = null;
        let postsData = [];

        // --- AUTHENTICATION ---
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const authScreen = document.getElementById('auth-screen');
        const appScreen = document.getElementById('app-screen');

        function toggleAuth() {
            loginForm.classList.toggle('hidden');
            registerForm.classList.toggle('hidden');
        }

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const u = document.getElementById('login-username').value;
            const p = document.getElementById('login-password').value;
            
            try {
                const res = await fetch(`${API_URL}/api/login`, {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: u, password: p})
                });
                const data = await res.json();
                if(data.token) {
                    currentUser = data.user;
                    initApp();
                } else {
                    alert(data.error);
                }
            } catch(err) { console.error(err); alert("Connection Error"); }
        });

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const u = document.getElementById('reg-username').value;
            const p = document.getElementById('reg-password').value;
            
            try {
                const res = await fetch(`${API_URL}/api/register`, {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: u, password: p})
                });
                const data = await res.json();
                if(data.message) {
                    alert("Registration Successful! Please Login.");
                    toggleAuth();
                } else {
                    alert(data.error);
                }
            } catch(err) { console.error(err); }
        });

        function logout() {
            currentUser = null;
            authScreen.classList.remove('hidden');
            appScreen.classList.add('hidden');
            loginForm.reset();
        }

        // --- APP LOGIC ---
        function initApp() {
            authScreen.classList.add('hidden');
            appScreen.classList.remove('hidden');
            
            // Set User Info
            document.getElementById('current-user-avatar').src = currentUser.avatar;
            document.getElementById('profile-img').src = currentUser.avatar;
            document.getElementById('profile-name').innerText = currentUser.username;
            document.getElementById('profile-bio').innerText = currentUser.bio;
            document.getElementById('profile-followers').innerText = currentUser.followers;
            document.getElementById('profile-following').innerText = currentUser.following;

            loadStories();
            loadFeed();
            loadExplore();
            loadProfilePosts();
        }

        async function loadStories() {
            const res = await fetch(`${API_URL}/api/stories`);
            const stories = await res.json();
            const container = document.getElementById('stories-wrapper');
            container.innerHTML = '';
            
            // Add "My Story" placeholder
            container.innerHTML += `
                <div class="story-item">
                    <div class="story-ring" style="border: 2px dashed #555; background: none; display:flex; align-items:center; justify-content:center;">
                        <i class="fa-solid fa-plus" style="color:white;"></i>
                    </div>
                    <span class="story-username">Add Story</span>
                </div>
            `;

            stories.forEach(s => {
                container.innerHTML += `
                    <div class="story-item">
                        <div class="story-ring">
                            <img src="${s.avatar}" alt="${s.username}">
                        </div>
                        <span class="story-username">${s.username}</span>
                    </div>
                `;
            });
        }

        async function loadFeed() {
            const res = await fetch(`${API_URL}/api/feed`);
            postsData = await res.json();
            renderPosts(postsData, 'feed-container');
        }

        async function loadExplore() {
            const res = await fetch(`${API_URL}/api/explore`);
            const posts = await res.json();
            const grid = document.getElementById('explore-grid');
            grid.innerHTML = '';
            posts.forEach(p => {
                grid.innerHTML += `
                    <div class="grid-item">
                        <img src="${p.media}" loading="lazy">
                        <div class="grid-overlay">
                            <span style="color:white"><i class="fa-solid fa-heart"></i> ${p.likes}</span>
                            <span style="color:white"><i class="fa-solid fa-comment"></i> ${p.comments.length}</span>
                        </div>
                    </div>
                `;
            });
        }

        function loadProfilePosts() {
            const myPosts = postsData.filter(p => p.userId === currentUser.id);
            document.getElementById('profile-posts').innerText = myPosts.length;
            const grid = document.getElementById('profile-grid');
            grid.innerHTML = '';
            myPosts.forEach(p => {
                grid.innerHTML += `<div class="grid-item"><img src="${p.media}"></div>`;
            });
        }

        function renderPosts(posts, containerId) {
            const container = document.getElementById(containerId);
            container.innerHTML = '';
            posts.forEach(post => {
                const isLiked = false; // In a real app, check user likes
                container.innerHTML += `
                    <div class="glass post-card">
                        <div class="post-header">
                            <img src="${post.avatar || 'https://via.placeholder.com/40'}" class="user-avatar">
                            <span class="username">${post.username}</span>
                            <i class="fa-solid fa-ellipsis" style="margin-left:auto; color:var(--text-muted); cursor:pointer;"></i>
                        </div>
                        ${post.type === 'image' ? `<img src="${post.media}" class="post-media">` : ''}
                        <div class="post-actions">
                            <i class="fa-regular fa-heart action-icon ${isLiked ? 'liked' : ''}" onclick="likePost(${post.id}, this)"></i>
                            <i class="fa-regular fa-comment action-icon" onclick="focusComment(${post.id})"></i>
                            <i class="fa-regular fa-paper-plane action-icon"></i>
                        </div>
                        <div class="post-content">
                            <span class="likes-count">${post.likes} likes</span>
                            <p><strong>${post.username}</strong> ${post.content}</p>
                            <div style="margin-top:5px; color:var(--text-muted); font-size:0.8rem;">View all ${post.comments.length} comments</div>
                        </div>
                    </div>
                `;
            });
        }

        async function createPost() {
            const content = document.getElementById('new-post-content').value;
            if(!content) return;

            await fetch(`${API_URL}/api/posts`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    userId: currentUser.id,
                    content: content,
                    type: 'text',
                    media: `https://picsum.photos/600/400?random=${Math.random()}` // Random image for demo
                })
            });
            document.getElementById('new-post-content').value = '';
            loadFeed(); // Refresh
            loadExplore();
        }

        async function likePost(postId, btn) {
            // Optimistic UI
            if(btn.classList.contains('liked')) {
                btn.classList.remove('liked');
                btn.classList.replace('fa-solid', 'fa-regular');
            } else {
                btn.classList.add('liked');
                btn.classList.replace('fa-regular', 'fa-solid');
            }

            await fetch(`${API_URL}/api/like/${postId}`, {method: 'POST'});
            // In a real app, re-fetch or update count accurately
            const likesSpan = btn.closest('.post-card').querySelector('.likes-count');
            let count = parseInt(likesSpan.innerText);
            likesSpan.innerText = (btn.classList.contains('liked') ? count + 1 : count - 1) + " likes";
        }

        function navTo(view) {
            // Hide all views
            ['feed', 'explore', 'notifications', 'profile'].forEach(v => {
                document.getElementById(`view-${v}`).classList.add('hidden');
            });
            // Show target
            document.getElementById(`view-${view}`).classList.remove('hidden');

            // Update Nav Active State (Desktop & Mobile)
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            // This is a simple selector, in production use IDs for nav items
            const navItems = document.querySelectorAll('.nav-item');
            if(view === 'feed') navItems[0].classList.add('active');
            if(view === 'explore') navItems[1].classList.add('active');
            if(view === 'notifications') navItems[2].classList.add('active');
            if(view === 'profile') navItems[3].classList.add('active');
            
            // Mobile nav specific
            const mobileNavs = document.querySelectorAll('.mobile-nav .nav-item');
            if(view === 'feed') mobileNavs[0].classList.add('active');
            if(view === 'explore') mobileNavs[1].classList.add('active');
            if(view === 'notifications') mobileNavs[2].classList.add('active');
            if(view === 'profile') mobileNavs[3].classList.add('active');
        }
    </script>
</body>
</html>
"""

# ==========================================
#               BACKEND ROUTES
# ==========================================

@app.route("/")
def home():
    return HTML_PAGE

# --- AUTH ---
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    # Simple check
    if any(u["username"] == data["username"] for u in users):
        return jsonify({"error": "Username taken"}), 400
    
    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "password": data["password"],
        "avatar": f"https://i.pravatar.cc/150?u={len(users)+1}",
        "bio": "New to the Nebula.",
        "followers": 0,
        "following": 0
    }
    users.append(new_user)
    return jsonify({"message": "User created"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    for user in users:
        if user["username"] == data["username"] and user["password"] == data["password"]:
            # Return user info (excluding password)
            user_resp = {k:v for k,v in user.items() if k != 'password'}
            return jsonify({"token": "fake-jwt-token", "user": user_resp})
    return jsonify({"error": "Invalid credentials"}), 401

# --- DATA ---
@app.route("/api/feed")
def feed():
    # Return posts with author info merged
    feed_data = []
    for post in posts:
        author = next((u for u in users if u["id"] == post["userId"]), None)
        if author:
            p = post.copy()
            p["avatar"] = author["avatar"]
            feed_data.append(p)
    return jsonify(feed_data)

@app.route("/api/stories")
def get_stories():
    return jsonify(stories)

@app.route("/api/explore")
def explore():
    # Return random posts for explore grid
    feed_data = []
    for post in posts:
        author = next((u for u in users if u["id"] == post["userId"]), None)
        if author:
            p = post.copy()
            p["avatar"] = author["avatar"]
            feed_data.append(p)
    # Shuffle for "explore" feel
    random.shuffle(feed_data)
    return jsonify(feed_data)

@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.json
    new_post = {
        "id": len(posts) + 1,
        "userId": data["userId"],
        "username": next((u["username"] for u in users if u["id"] == data["userId"]), "Unknown"),
        "avatar": next((u["avatar"] for u in users if u["id"] == data["userId"]), ""),
        "type": data.get("type", "text"),
        "media": data.get("media"),
        "content": data.get("content"),
        "likes": 0,
        "comments": []
    }
    posts.insert(0, new_post)
    return jsonify(new_post)

@app.route("/api/like/<int:post_id>", methods=["POST"])
def like(post_id):
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            return jsonify({"likes": post["likes"]})
    return jsonify({"error": "Not found"}), 404

# --- PROFILE ---
@app.route("/api/profile/<username>")
def profile(username):
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_posts = [p for p in posts if p["userId"] == user["id"]]
    return jsonify({
        "user": user,
        "posts": user_posts
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # threaded=True allows handling multiple requests
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
