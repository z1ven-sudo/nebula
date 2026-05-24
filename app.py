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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nebula | Ijtimoiy Tarmoqning Kelajagi</title>
    
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        /* --- CSS O'ZGARUVCHILARI VA Mavzu --- */
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

        /* --- ASOSIY SOZLAMALAR --- */
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

        /* --- YORDAMCHI KLASSLAR --- */
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
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px var(--primary-glow);
            width: 100%;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 25px var(--primary-glow); }
        
        .btn-icon { background: transparent; color: var(--text-main); font-size: 1.2rem; padding: 8px; border-radius: 50%; transition: background 0.2s; }
        .btn-icon:hover { background: rgba(255,255,255,0.1); }
        .btn-icon.active { color: var(--danger-color); } /* Like rangi qizil */

        .avatar { border-radius: 50%; border: 2px solid var(--border-color); }
        .avatar.online { border-color: var(--success-color); box-shadow: 0 0 8px var(--success-color); }
        
        .badge { 
            background: var(--primary-color); color: white; font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; margin-left: 4px; vertical-align: middle;
        }
        
        .hidden { display: none !important; }

        /* --- LAYOUT TIZIMI --- */
        #app {
            display: none; /* Dastlab yashirin, login bo'lgach ochiladi */
            flex: 1;
            height: 100%;
            overflow: hidden;
            position: relative;
        }

        /* Yon panel (Desktop) */
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

        .logo { font-size: 1.8rem; font-weight: 700; margin-bottom: 40px; display: flex; align-items: center; gap: 10px; cursor: pointer;}
        .logo i { color: var(--accent-color); text-shadow: 0 0 10px var(--accent-glow); }

        .nav-links { display: flex; flex-direction: column; gap: 10px; }
        .nav-item { display: flex; align-items: center; gap: 15px; font-size: 1.1rem; padding: 12px; border-radius: 12px; transition: all 0.2s; color: var(--text-muted); }
        .nav-item:hover, .nav-item.active { background: rgba(255,255,255,0.05); color: var(--text-main); }
        .nav-item i { width: 24px; text-align: center; }

        /* Asosiy kontent */
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

        /* Mobil qismi */
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

        .mobile-nav {
            display: none;
            height: var(--nav-height);
            border-top: var(--glass-border);
            justify-content: space-around;
            align-items: center;
            z-index: 100;
        }

        /* --- KOMPONENTLAR --- */
        
        /* History (Stories) */
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
            transition: transform 0.2s;
        }
        .story-circle:hover .ring { transform: scale(1.05); }
        .ring img { width: 100%; height: 100%; border-radius: 50%; border: 3px solid var(--bg-color); }
        .story-name { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 70px; }

        /* Post Kartasi */
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
        
        .post-media { width: 100%; background: #000; display: flex; align-items: center; justify-content: center; position: relative; min-height: 200px;}
        .post-media img, .post-media video { width: 100%; max-height: 600px; display: block; }
        
        .post-actions { padding: 12px; display: flex; justify-content: space-between; font-size: 1.4rem; }
        .action-group { display: flex; gap: 15px; }
        
        .post-content { padding: 0 12px 12px; }
        .likes-count { font-weight: 600; margin-bottom: 6px; display: block; cursor: pointer; }
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

        /* Post yaratish maydoni */
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
            transition: background 0.3s;
        }
        .create-input:hover { background: rgba(255,255,255,0.1); }

        /* Auth Sahifalari (Login/Register) */
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
            position: relative;
            overflow: hidden;
        }
        .auth-input {
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: white;
            transition: 0.3s;
        }
        .auth-input:focus { border-color: var(--primary-color); box-shadow: 0 0 10px var(--primary-glow); }
        
        .auth-switch {
            margin-top: 20px;
            font-size: 0.9rem;
            color: var(--text-muted);
        }
        .auth-switch span {
            color: var(--primary-color);
            cursor: pointer;
            font-weight: 600;
        }
        
        /* Xabar (Toast) */
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
            padding: 12px 24px;
            border-radius: 30px;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

        /* Explore Grid */
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
        .grid-item img {
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

        /* Profil Sahifasi */
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
        .btn-secondary { background: rgba(255,255,255,0.1); color: white; padding: 8px 20px; border-radius: 20px; font-weight: 500; border: 1px solid transparent; transition: 0.3s;}
        .btn-secondary:hover { border-color: var(--primary-color); }

        /* Responsive */
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .mobile-nav, .mobile-header { display: flex; }
            .feed-container { padding: 10px; margin-bottom: 70px; }
            .grid-gallery { gap: 1px; }
            .auth-box { padding: 20px; border: none; background: transparent; box-shadow: none; width: 90%; }
        }

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
        .close-modal { position: absolute; top: 15px; right: 15px; cursor: pointer; color: var(--text-muted); font-size: 1.2rem; }

    </style>
</head>
<body>

    <!-- --- ASOSIY ILOVA (Login bo'lganda ko'rinadi) --- -->
    <div id="app">
        
        <!-- Desktop Sidebar -->
        <aside class="sidebar glass">
            <div>
                <div class="logo neon-text-purple" onclick="router.navigate('home')">
                    <i class="fa-solid fa-atom"></i> Nebula
                </div>
                <nav class="nav-links">
                    <a href="#" class="nav-item active" onclick="router.navigate('home')"><i class="fa-solid fa-house"></i> Bosh sahifa</a>
                    <a href="#" class="nav-item" onclick="router.navigate('explore')"><i class="fa-solid fa-compass"></i> Qidirish</a>
                    <a href="#" class="nav-item" onclick="router.navigate('reels')"><i class="fa-brands fa-tiktok"></i> Reels</a>
                    <a href="#" class="nav-item" onclick="router.navigate('messages')"><i class="fa-solid fa-paper-plane"></i> Xabarlar</a>
                    <a href="#" class="nav-item" onclick="router.navigate('notifications')"><i class="fa-solid fa-heart"></i> Bildirishnomalar</a>
                    <a href="#" class="nav-item" onclick="router.navigate('profile')"><i class="fa-solid fa-user"></i> Profil</a>
                </nav>
            </div>
            <div class="nav-item" onclick="app.logout()"><i class="fa-solid fa-right-from-bracket"></i> Chiqish</div>
        </aside>

        <!-- Asosiy Kontent -->
        <main class="main-content" id="main-scroll">
            <!-- Mobil Header -->
            <header class="mobile-header glass">
                <div class="logo" style="font-size: 1.5rem; margin:0;">
                    <i class="fa-solid fa-atom neon-text-cyan"></i>
                </div>
                <div style="display: flex; gap: 15px;">
                    <i class="fa-solid fa-plus-square" onclick="ui.openCreateModal()"></i>
                    <i class="fa-solid fa-bars" onclick="ui.toast('Menu tez orada qo\'shiladi')"></i>
                </div>
            </header>

            <!-- Dynamic View Container -->
            <div id="view-container">
                <!-- JS orqali to'ldiriladi -->
            </div>
        </main>

        <!-- Mobil Pastki Menyu -->
        <nav class="mobile-nav glass">
            <a href="#" onclick="router.navigate('home')"><i class="fa-solid fa-house fa-lg"></i></a>
            <a href="#" onclick="router.navigate('explore')"><i class="fa-solid fa-compass fa-lg"></i></a>
            <a href="#" onclick="router.navigate('reels')"><i class="fa-brands fa-tiktok fa-lg"></i></a>
            <a href="#" onclick="router.navigate('messages')"><i class="fa-solid fa-paper-plane fa-lg"></i></a>
            <a href="#" onclick="router.navigate('profile')"><i class="fa-solid fa-user fa-lg"></i></a>
        </nav>
    </div>

    <!-- --- AUTH TIZIMI (Login/Register) --- -->
    <div id="auth-container" class="auth-container">
        
        <!-- LOGIN FORM -->
        <div id="login-form" class="auth-box glass">
            <div class="logo neon-text-cyan" style="justify-content: center; margin-bottom: 20px;">
                <i class="fa-solid fa-atom"></i> Nebula
            </div>
            <h2 style="margin-bottom: 10px;">Xush kelibsiz</h2>
            <p style="color: var(--text-muted); margin-bottom: 30px;">Koinotga qo'shiling.</p>
            
            <form onsubmit="app.handleLogin(event)">
                <input type="text" id="login-username" class="auth-input" placeholder="Foydalanuvchi nomi" required>
                <input type="password" id="login-password" class="auth-input" placeholder="Parol" required>
                <button type="submit" class="btn-primary" style="margin-top: 10px;">Kirish</button>
            </form>
            <div class="auth-switch">
                Hisobingiz yo'qmi? <span onclick="ui.toggleAuth('register')">Ro'yxatdan o'tish</span>
            </div>
            <p style="margin-top:15px; font-size: 0.8rem; color: #555;">Demo: user / 1234</p>
        </div>

        <!-- REGISTER FORM -->
        <div id="register-form" class="auth-box glass hidden">
            <div class="logo neon-text-purple" style="justify-content: center; margin-bottom: 20px;">
                <i class="fa-solid fa-atom"></i> Ro'yxatdan o'tish
            </div>
            <h2 style="margin-bottom: 10px;">Hisob yaratish</h2>
            <p style="color: var(--text-muted); margin-bottom: 20px;">Yangi akkaunt oching.</p>
            
            <form onsubmit="app.handleRegister(event)">
                <input type="text" id="reg-username" class="auth-input" placeholder="Foydalanuvchi nomi" required>
                <input type="email" id="reg-email" class="auth-input" placeholder="Email" required>
                <input type="password" id="reg-password" class="auth-input" placeholder="Parol" required>
                <button type="submit" class="btn-primary" style="margin-top: 10px;">Yaratish</button>
            </form>
            <div class="auth-switch">
                Allaqachon hisobingiz bormi? <span onclick="ui.toggleAuth('login')">Kirish</span>
            </div>
        </div>
    </div>

    <!-- Xabarlar joyi -->
    <div class="toast-container" id="toast-container"></div>

    <!-- Post Yaratish Modali -->
    <div class="modal-overlay" id="create-modal">
        <div class="modal-content glass">
            <i class="fa-solid fa-xmark close-modal" onclick="ui.closeModals()"></i>
            <h3 style="margin-bottom: 15px;">Yangi Post</h3>
            <textarea id="new-post-content" rows="4" class="auth-input" placeholder="O'ylayotgan narsangiz nima?"></textarea>
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <button class="btn-secondary" onclick="document.getElementById('file-upload').click()"><i class="fa-solid fa-image"></i> Rasm</button>
                <input type="file" id="file-upload" hidden onchange="ui.handleFileSelect(this)">
                <span id="file-name" style="font-size: 0.8rem; color: var(--text-muted); padding: 8px;"></span>
            </div>
            <button class="btn-primary" style="margin-top: 20px;" onclick="app.createPost()">Post Qilish</button>
        </div>
    </div>
<form onsubmit="app.handleLogin(event)">
<form onsubmit="return app.handleLogin(event)">
<form onsubmit="return app.handleRegister(event)">
    <!-- --- JAVASCRIPT LOGIC --- -->
    <script>
      
     
const API = "https://SENING-RAILWAY-LINKING.up.railway.app";

        // --- MOCK DATABASE (Boshlang'ich ma'lumotlar) ---
        const defaultDB = {
            users: [
                { id: 1, username: 'user', password: '123', avatar: 'https://picsum.photos/seed/user/200', verified: true, bio: 'Demo foydalanuvchi. 🌌', followers: 1250, following: 340 },
                { id: 2, username: 'neon_wolf', password: '123', avatar: 'https://picsum.photos/seed/neon/200', verified: true, bio: 'Cyberpunk enthusiast.', followers: 500, following: 120 },
                { id: 3, username: 'designer', password: '123', avatar: 'https://picsum.photos/seed/design/200', verified: false, bio: 'UI/UX Lover.', followers: 8900, following: 45 }
            ],
            posts: [
                { id: 101, userId: 1, type: 'image', media: 'https://picsum.photos/seed/p1/600/600', content: 'Bugun juda chiroyli kun! 🌃✨ #cyberpunk', likes: 120, comments: [{user: 'neon_wolf', text: 'Awesome!'}], timestamp: '2h oldin' },
                { id: 102, userId: 3, type: 'image', media: 'https://picsum.photos/seed/p2/600/800', content: 'Yangi dizayn loyihasi. 🎨', likes: 543, comments: [], timestamp: '5h oldin' }
            ],
            stories: [
                { id: 1, userId: 2, img: 'https://picsum.photos/seed/s1/300', viewed: false },
                { id: 2, userId: 3, img: 'https://picsum.photos/seed/s2/300', viewed: false }
            ],
            currentUser: null
        };

        // Global DB objekti
        let db = {};

        // --- APP CONTROLLER ---
        const app = {
            init: () => {
                // Ma'lumotlarni yuklash
                storage.load();
                
                // Sessiyani tekshirish
                const sessionUser = sessionStorage.getItem('nebula_session');
                if (sessionUser) {
                    db.currentUser = JSON.parse(sessionUser);
                    app.loadApp();
                } else {
                    // Agar login bo'lmagan auth ko'rsatish
                    document.getElementById('auth-container').style.display = 'flex';
                }
            },

            // Ro'yxatdan o'tish logikasi

handleRegister: (e) => {
    e.preventDefault();

    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    if (db.users.find(u => u.username === username)) {
        ui.toast('Bu username band qilingan!', 'error');
        return;
    }

    const newUser = {
        id: Date.now(),
        username: username,
        email: email,
        password: password,
        avatar: `https://picsum.photos/seed/${username}/200`,
        verified: false,
        bio: 'Yangi foydalanuvchi',
        followers: 0,
        following: 0
    };

    db.users.push(newUser);
    storage.save();

    ui.toast('Muvaffaqiyatli ro‘yxatdan o‘tdingiz!');

    db.currentUser = newUser;
    sessionStorage.setItem('nebula_session', JSON.stringify(newUser));

    document.getElementById('auth-container').style.display = 'none';
    app.loadApp();
},
                
                
            // Kirish logikasi
            handleLogin: (e) => {
                e.preventDefault();
                const username = document.getElementById('login-username').value;
                const password = document.getElementById('login-password').value;

                const user = db.users.find(u => u.username === username && u.password === password);
                
                if (user) {
                    db.currentUser = user;
                    sessionStorage.setItem('nebula_session', JSON.stringify(user));
                    ui.toast('Xush kelibsiz, ' + user.username);
                    document.getElementById('auth-container').style.display = 'none';
                    app.loadApp();
                } else {
                    ui.toast('Login yoki parol noto\'g\'ri!', 'error');
                }
            },

            logout: () => {
                sessionStorage.removeItem('nebula_session');
                location.reload();
            },

            loadApp: () => {
                document.getElementById('app').style.display = 'flex';
                router.navigate('home');
            },

            // Post yaratish
            createPost: () => {
                const content = document.getElementById('new-post-content').value;
                const fileInput = document.getElementById('file-upload');
                let mediaUrl = null;
                let type = 'text';

                // Agar rasm tanlangan bo'lsa (bu yerda mock URL)
                if(fileInput.files.length > 0) {
                    // Haqiqiy yuklash uchun server kerak, shu sababli random rasm qo'yamiz demo uchun
                    mediaUrl = `https://picsum.photos/seed/${Date.now()}/600/600`;
                    type = 'image';
                } else if (content.trim() === '') {
                    ui.toast('Iltimos, matn kiriting!', 'error');
                    return;
                }

                const newPost = {
                    id: Date.now(),
                    userId: db.currentUser.id,
                    type: type,
                    media: mediaUrl,
                    content: content,
                    likes: 0,
                    comments: [],
                    timestamp: 'Hozirgina'
                };
                
                // DBga qo'shish
                db.posts.unshift(newPost);
                storage.save(); // Postni saqlash (refresh bo'lsa ham qoladi)
                
                ui.closeModals();
                ui.toast('Post joylandi!');
                document.getElementById('new-post-content').value = '';
                fileInput.value = '';
                document.getElementById('file-name').innerText = '';
                
                // Feedni yangilash
                if(router.current === 'home') router.renderHome();
            },

            toggleLike: (id, btn) => {
                const icon = btn.querySelector('i');
                const post = db.posts.find(p => p.id === id);
                if(post) {
                    if (icon.classList.contains('fa-regular')) {
                        // Like
                        icon.classList.remove('fa-regular');
                        icon.classList.add('fa-solid');
                        btn.classList.add('active');
                        post.likes++;
                    } else {
                        // Unlike
                        icon.classList.remove('fa-solid');
                        icon.classList.add('fa-regular');
                        btn.classList.remove('active');
                        post.likes--;
                    }
                    // UI yangilash
                    const counter = btn.closest('.post').querySelector('.likes-count');
                    counter.innerText = post.likes + ' likes';
                    storage.save(); // O'zgarishlarni saqlash
                }
            }
        };

        // --- XOTIRA (Storage) MANAGERI ---
        const storage = {
            load: () => {
                const savedUsers = localStorage.getItem('nebula_users');
                const savedPosts = localStorage.getItem('nebula_posts');
                
                if (savedUsers) {
                    db.users = JSON.parse(savedUsers);
                } else {
                    db.users = defaultDB.users; // Default users
                }

                if (savedPosts) {
                    db.posts = JSON.parse(savedPosts);
                } else {
                    db.posts = defaultDB.posts; // Default posts
                }
                
                db.stories = defaultDB.stories; // Stories vaqtinchalik
            },
            save: () => {
                localStorage.setItem('nebula_users', JSON.stringify(db.users));
                localStorage.setItem('nebula_posts', JSON.stringify(db.posts));
            }
        };

        // --- ROUTER & VIEWs ---
        const router = {
            current: 'home',
            
            navigate: (route) => {
                router.current = route;
                const container = document.getElementById('view-container');
                
                // Nav active klassi
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                // Oddiy tanlash (haqiqiy loyihada attribute orqali qilinadi)
                
                if (route === 'home') router.renderHome();
                else if (route === 'explore') router.renderExplore();
                else if (route === 'reels') router.renderReels();
                else if (route === 'profile') router.renderProfile();
                else if (route === 'messages') router.renderMessages();
                else if (route === 'notifications') router.renderNotifications();
                
                // Sahifani yuqoriga ko'tarish
                document.getElementById('main-scroll').scrollTop = 0;
            },

            renderHome: () => {
                const container = document.getElementById('view-container');
                
                // Stories
                let storiesHtml = `<div class="stories-wrapper">
                    <div class="story-circle">
                        <div class="ring" style="border: 2px dashed var(--text-muted); background: none; display:flex; align-items:center; justify-content:center;">
                            <i class="fa-solid fa-plus" style="font-size: 1.5rem; color:white;"></i>
                        </div>
                        <span class="story-name">Story</span>
                    </div>`;
                
                db.stories.forEach(s => {
                    const user = db.users.find(u => u.id === s.userId);
                    if(user) {
                        storiesHtml += `
                            <div class="story-circle" onclick="ui.viewStory(${s.id})">
                                <div class="ring" style="background: ${s.viewed ? '#333' : 'linear-gradient(45deg, var(--primary-color), var(--accent-color))'}">
                                    <img src="${user.avatar}" alt="${user.username}">
                                </div>
                                <span class="story-name">${user.username}</span>
                            </div>`;
                    }
                });
                storiesHtml += `</div>`;

                // Posts
                let postsHtml = `<div class="feed-container">
                    <div class="create-post-card">
                        <img src="${db.currentUser.avatar}" class="avatar" width="40" height="40">
                        <input type="text" class="create-input" placeholder="Nima gapirishni xohlaysiz?" readonly onclick="ui.openCreateModal()">
                    </div>
                    ${storiesHtml}
                `;

                db.posts.forEach(post => {
                    const user = db.users.find(u => u.id === post.userId);
                    if(!user) return; // Xavfsizlik

                    const verifiedBadge = user.verified ? `<i class="fa-solid fa-circle-check badge" style="color: var(--accent-color); background:none;"></i>` : '';
                    const isLiked = false; // Backendda bo'lishi kerak edi, hozircha UI
                    
                    let mediaHtml = '';
                    if(post.type === 'image' && post.media) {
                        mediaHtml = `<img src="${post.media}" alt="Post Content" loading="lazy">`;
                    }

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
                                <span class="comments-link">Barcha ${post.comments.length} sharxni ko'rish</span>
                            </div>
                        </article>
                    `;
                });
                postsHtml += `</div>`;
                container.innerHTML = postsHtml;
            },

            renderExplore: () => {
                const container = document.getElementById('view-container');
                let html = `<div class="feed-container"><h2 style="margin-bottom:15px;">Qidirish</h2><div class="grid-gallery">`;
                // Random rasmlar
                for(let i=0; i<12; i++) {
                    html += `
                        <div class="grid-item">
                            <img src="https://picsum.photos/seed/explore${i}/400/400">
                            <div class="grid-overlay">
                                <i class="fa-solid fa-heart"></i> ${Math.floor(Math.random()*500)}
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
                        <p>Tez orada...</p>
                    </div>
                `;
            },

            renderProfile: () => {
                const u = db.currentUser;
                const container = document.getElementById('view-container');
                
                // Foydalanuvchi postlari
                let gridHtml = `<div class="grid-gallery" style="max-width:600px; margin:0 auto;">`;
                db.posts.filter(p => p.userId === u.id).forEach(p => {
                     gridHtml += `<div class="grid-item"><img src="${p.media || 'https://picsum.photos/seed/'+p.id+'/400'}"></div>`;
                });
                if(gridHtml === `<div class="grid-gallery" style="max-width:600px; margin:0 auto;">`) {
                    gridHtml += `<p style="grid-column: 1/-1; text-align:center; padding: 20px;">Hali post yo'q.</p>`;
                }
                gridHtml += `</div>`;

                container.innerHTML = `
                    <div class="glass" style="min-height: 100%; padding-bottom: 50px;">
                        <div class="profile-header">
                            <img src="${u.avatar}" class="profile-avatar-large">
                            <h2>${u.username} ${u.verified ? '<i class="fa-solid fa-circle-check badge" style="background:none; color:var(--accent-color)"></i>' : ''}</h2>
                            <p style="color:var(--text-muted); margin-top: 5px;">${u.bio}</p>
                            
                            <div class="profile-stats">
                                <div class="stat-box"><span class="stat-num">${db.posts.filter(p => p.userId === u.id).length}</span><span class="stat-label">Postlar</span></div>
                                <div class="stat-box"><span class="stat-num">${u.followers}</span><span class="stat-label">Followers</span></div>
                                <div class="stat-box"><span class="stat-num">${u.following}</span><span class="stat-label">Following</span></div>
                            </div>

                            <div class="profile-actions">
                                <button class="btn-secondary">Tahrirlash</button>
                                <button class="btn-secondary"><i class="fa-solid fa-share"></i></button>
                            </div>
                        </div>
                        
                        <div style="display:flex; border-bottom: 1px solid var(--border-color); margin-top: 10px;">
                            <div style="flex:1; text-align:center; padding:15px; border-bottom: 2px solid white;"><i class="fa-solid fa-grid"></i></div>
                            <div style="flex:1; text-align:center; padding:15px; color:var(--text-muted);"><i class="fa-solid fa-bookmark"></i></div>
                        </div>

                        ${gridHtml}
                    </div>
                `;
            },

            renderMessages: () => {
                const container = document.getElementById('view-container');
                container.innerHTML = `<div class="feed-container" style="text-align:center; padding-top:50px;"><h3>Xabarlar</h3><p>Tez orada qo'shiladi</p></div>`;
            },

            renderNotifications: () => {
                const container = document.getElementById('view-container');
                container.innerHTML = `<div class="feed-container" style="text-align:center; padding-top:50px;"><h3>Bildirishnomalar</h3><p>Hozircha yo'q</p></div>`;
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

            toggleAuth: (type) => {
                const loginForm = document.getElementById('login-form');
                const regForm = document.getElementById('register-form');
                
                if(type === 'register') {
                    loginForm.classList.add('hidden');
                    regForm.classList.remove('hidden');
                } else {
                    regForm.classList.add('hidden');
                    loginForm.classList.remove('hidden');
                }
            },

            openCreateModal: () => {
                document.getElementById('create-modal').style.display = 'flex';
            },

            closeModals: () => {
                document.querySelectorAll('.modal-overlay').forEach(el => el.style.display = 'none');
            },
            
            handleFileSelect: (input) => {
                const fileName = input.files[0] ? input.files[0].name : '';
                document.getElementById('file-name').innerText = fileName;
            },

            viewStory: (id) => {
                const s = db.stories.find(x => x.id === id);
                const user = db.users.find(u => u.id === s.userId);
                
                // Fullscreen story overlay
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
                        <div style="position:absolute; top:10px; left:10px; right:10px; height:2px; background:rgba(255,255,255,0.3); border-radius:2px;">
                            <div style="width:100%; height:100%; background:white; animation: storyProgress 5s linear forwards;"></div>
                        </div>
                        <style>@keyframes storyProgress { from {width:0%} to {width:100%} }</style>
                    </div>
                `;
                document.body.appendChild(overlay);
                setTimeout(() => { if(overlay.parentNode) overlay.remove(); }, 5000);
            }
        };

        handleLogin: async (e) => {
    e.preventDefault();
    ...
    return false;
},

handleRegister: async (e) => {
    e.preventDefault();
    ...
    return false;
},

        // --- INIT ---
        window.addEventListener('load', app.init);

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
