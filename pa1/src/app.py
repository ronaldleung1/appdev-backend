import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
      "id": 0,
      "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98",
    },
    1: {
      "id": 1,
      "upvotes": 3,
      "title": "Cat loaf",
      "link": "https://i.imgur.com/TJ46wX4.jpg",
      "username": "alicia98",
    }
}

post_current_id = len(posts) - 1

@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here
@app.route("/api/posts", methods=["GET"])
def get_posts():
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route("/api/posts", methods=["POST"])
def create_post():
    global post_current_id
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    post_current_id += 1
    post = {
        "id": post_current_id,
        "upvotes": 0,
        "title": title,
        "link": link,
        "username": username,
    }
    posts[post_current_id] = post
    return json.dumps(post), 201

@app.route("/api/posts/<int:post_id>/", methods=["GET"])
def get_one_post(post_id):
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
