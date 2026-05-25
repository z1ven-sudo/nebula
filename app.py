from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MEMORY DB
users = []
posts = []

# MODELS
class User(BaseModel):
    username: str
    password: str

class Post(BaseModel):
    userId: int
    image: str
    caption: str

# TEST
@app.get("/")
def home():
    return {"status": "Nebula backend working"}

# REGISTER
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

# LOGIN
@app.post("/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            return u

    return {"error": "Invalid credentials"}

# GET POSTS
@app.get("/posts")
def get_posts():
    return posts

# CREATE POST
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
