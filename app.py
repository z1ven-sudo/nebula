from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- MEMORY DB (server ichida) ---
users = []
posts = []

# --- MODELS ---
class User(BaseModel):
    username: str
    password: str

class Post(BaseModel):
    userId: int
    image: str
    caption: str

# -------------------
# REGISTER
# -------------------
@app.post("/register")
def register(user: User):
    for u in users:
        if u["username"] == user.username:
            return {"error": "Username exists"}

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
        "password": user.password,
        "avatar": f"https://picsum.photos/seed/{user.username}/100/100"
    }

    users.append(new_user)
    return new_user

# -------------------
# LOGIN
# -------------------
@app.post("/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            return u

    return {"error": "Invalid credentials"}

# -------------------
# GET POSTS
# -------------------
@app.get("/posts")
def get_posts():
    return posts

# -------------------
# CREATE POST
# -------------------
@app.post("/posts")
def create_post(post: Post):
    new_post = {
        "id": len(posts) + 1,
        "userId": post.userId,
        "image": post.image,
        "caption": post.caption,
        "likes": 0,
        "comments": []
    }

    posts.insert(0, new_post)
    return new_post
