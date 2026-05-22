import os
import datetime
import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nebula.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(500), default='')

    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
            'avatar': self.avatar
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.author.to_dict(),
            'image': self.image,
            'caption': self.caption,
            'likes': len(self.likes),
            'timestamp': int(self.timestamp.timestamp() * 1000)
        }


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.author.username,
            'text': self.text
        }

# ---------------- TOKEN ----------------
active_tokens = {}

def get_current_user():
    token = request.headers.get('Authorization')
    if not token or token not in active_tokens:
        return None
    return User.query.get(active_tokens[token])

# ---------------- SEED DATA ----------------
def seed_data():
    if User.query.count() == 0:
        names = ['alex_designs', 'sarah_travels', 'tech_guru']

        for name in names:
            user = User(
                username=name,
                email=f"{name}@test.com",
                fullname=name.upper(),
                password=generate_password_hash('password'),
                avatar=f"https://picsum.photos/seed/{name}/200/200"
            )
            db.session.add(user)

        db.session.commit()

        # demo postlar
        users = User.query.all()
        for i, user in enumerate(users):
            post = Post(
                user_id=user.id,
                image=f"https://picsum.photos/seed/post{i}/600/600",
                caption=f"Hello Nebula #{i}"
            )
            db.session.add(post)

        db.session.commit()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return "NebulaSocial backend ishlayapti 🚀"


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email exists'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        fullname=data['fullname'],
        password=generate_password_hash(data['password']),
        avatar=f"https://picsum.photos/seed/{data['username']}/200/200"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict())


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        token = str(user.id) + "_" + str(random.randint(1000, 9999))
        active_tokens[token] = user.id

        return jsonify({'token': token, 'user': user.to_dict()})

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([p.to_dict() for p in posts])


@app.route('/api/posts', methods=['POST'])
def create_post():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json

    post = Post(
        user_id=user.id,
        image=data['image'],
        caption=data['caption']
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict())


@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
def like(post_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    like = Like.query.filter_by(user_id=user.id, post_id=post_id).first()

    if like:
        db.session.delete(like)
    else:
        db.session.add(Like(user_id=user.id, post_id=post_id))

    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def comment(post_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json

    c = Comment(
        user_id=user.id,
        post_id=post_id,
        text=data['text']
    )

    db.session.add(c)
    db.session.commit()

    return jsonify(c.to_dict())
    

# ---------------- RUN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()

    print("Server http://127.0.0.1:5000 ishlayapti 🚀")
    app.run(debug=True, port=5000)