from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MEMORY DATABASE ----------------
users = []
posts = []

# ---------------- MODELS ----------------
class User(BaseModel):
    username: str
    password: str


class LoginModel(BaseModel):
    username: str
    password: str


class PostModel(BaseModel):
    userId: int
    image: str
    caption: str


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Nebula backend running"
    }


# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: User):

    for u in users:
        if u["username"] == user.username:
            return {
                "success": False,
                "message": "Username already exists"
            }

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
        "password": user.password,
        "avatar": f"https://picsum.photos/seed/{user.username}/100/100",
        "bio": "New Nebula user 🚀",
        "followers": 0,
        "following": 0
    }

    users.append(new_user)

    return {
        "success": True,
        "user": new_user
    }


# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: LoginModel):

    for user in users:
        if (
            user["username"] == data.username
            and user["password"] == data.password
        ):
            return {
                "success": True,
                "user": user
            }

    return {
        "success": False,
        "message": "Invalid username or password"
    }


# ---------------- GET USERS ----------------
@app.get("/users")
def get_users():
    return users


# ---------------- CREATE POST ----------------
@app.post("/posts")
def create_post(post: PostModel):

    new_post = {
        "id": len(posts) + 1,
        "userId": post.userId,
        "image": post.image,
        "caption": post.caption,
        "likes": 0,
        "comments": []
    }

    posts.insert(0, new_post)

    return {
        "success": True,
        "post": new_post
    }


# ---------------- GET POSTS ----------------
@app.get("/posts")
def get_posts():
    return posts


# ---------------- LIKE POST ----------------
@app.post("/posts/{post_id}/like")
def like_post(post_id: int):

    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1

            return {
                "success": True,
                "likes": post["likes"]
            }

    return {
        "success": False,
        "message": "Post not found"
    }


# ---------------- ADD COMMENT ----------------
@app.post("/posts/{post_id}/comment")
def add_comment(post_id: int, comment: dict):

    for post in posts:
        if post["id"] == post_id:

            post["comments"].append(comment)

            return {
                "success": True,
                "comments": post["comments"]
            }

    return {
        "success": False,
        "message": "Post not found"
    }


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
