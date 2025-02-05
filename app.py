from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Path for posts file
POSTS_FILE = "posts.json"

# Load posts from JSON file
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save posts to JSON file
def save_posts(posts):
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Both Title and Content are required!")
            return redirect(url_for("create"))

        posts = load_posts()
        post_id = len(posts) + 1
        posts.append({"id": post_id, "title": title, "content": content})
        save_posts(posts)

        flash("Post created successfully!")
        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    posts = load_posts()
    post = next((post for post in posts if post["id"] == post_id), None)
    if not post:
        flash("Post not found!")
        return redirect(url_for("index"))
    return render_template("post_detail.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
