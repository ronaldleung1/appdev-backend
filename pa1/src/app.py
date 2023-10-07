import json

from flask import Flask
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
        "comments": {
            0: {
                "id": 0,
                "upvotes": 8,
                "text": "Wow, my first Reddit gold!",
                "username": "alicia98",
            },
        },
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
        "comments": {},
    },
}

post_current_id = 1
comment_current_id = 0


@app.route("/")
def hello_world():
    return "Hello world!"


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Get all posts
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200


@app.route("/api/posts", methods=["POST"])
def create_post():
    """
    Create a post
    """
    global post_current_id
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if title is None or link is None or username is None:
        return json.dumps({"error": "Bad Request"}), 400

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
    """
    Get a specific post
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200


@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Delete a specific post
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    del posts[post_id]
    return json.dumps(post), 200


@app.route("/api/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):
    """
    Get comments for a specific post
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    res = {"comments": list(post.get("comments").values())}
    return json.dumps(res), 200


@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def post_comment(post_id):
    """
    Post a comment for a specific post
    """
    global comment_current_id
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404

    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")
    if text is None or username is None:
        return json.dumps({"error": "Bad Request"}), 400

    comment_current_id += 1
    comment = {
        "id": comment_current_id,
        "upvotes": 1,
        "text": text,
        "username": username,
    }
    post["comments"][comment_current_id] = comment
    return json.dumps(comment), 201


@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>", methods=["PUT"])
def edit_comment(post_id, comment_id):
    """
    Edit a comment for a specific post
    """
    post = posts.get(post_id)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404

    comment = post.get("comments").get(comment_id)
    if comment is None:
        return json.dumps({"error": "Comment not found"}), 404

    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Bad Request"}), 400
    comment["text"] = text
    return json.dumps(comment), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
