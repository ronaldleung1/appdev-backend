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
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
    },
}

comments = {
    0: {
        "id": 0,
        "post_id": 0,
        "upvotes": 8,
        "text": "Wow, my first Reddit gold!",
        "username": "alicia98",
    },
    1: {
        "id": 1,
        "post_id": 1,
        "upvotes": 10,
        "text": "Wow, my second Reddit gold!",
        "username": "alicia98",
    },
    2: {
        "id": 2,
        "post_id": 1,
        "upvotes": 2,
        "text": "Wow what a big deal *rolls eyes*",
        "username": "troll21",
    },
}


post_current_id = 1
comment_current_id = 2


@app.route("/api/posts/", methods=["GET"])
def get_posts():
    """
    Get all posts
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200


@app.route("/api/posts/", methods=["POST"])
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
        "upvotes": 1,
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


@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_comments(post_id):
    """
    Get comments for a specific post
    """
    # check if post exists
    if post_id not in posts:
        return json.dumps({"error": "Post not found"}), 404
    
    # filter comments by post_id
    comments_list = comments.values()
    filtered_comments = list(filter(lambda c: c["post_id"] == post_id, comments_list))
    res = {"comments": []}
    for comment in filtered_comments:
        res["comments"].append({
            "id": comment["id"],
            "upvotes": comment["upvotes"],
            "text": comment["text"],
            "username": comment["username"]
        })
    return json.dumps(res), 200


@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def post_comment(post_id):
    """
    Post a comment for a specific post
    """
    global comment_current_id
    
    # check if post exists
    if post_id not in posts:
        return json.dumps({"error": "Post not found"}), 404

    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")
    if text is None or username is None:
        return json.dumps({"error": "Bad Request"}), 400

    comment_current_id += 1
    comment = {
        "id": comment_current_id,
        "post_id": post_id,
        "upvotes": 1,
        "text": text,
        "username": username,
    }
    comments[comment_current_id] = comment
    return json.dumps({
        "id": comment_current_id,
        "upvotes": 1,
        "text": text,
        "username": username
    })


@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["PUT"])
def edit_comment(post_id, comment_id):
    """
    Edit a comment for a specific post
    """
    # check if post exists
    if post_id not in posts:
        return json.dumps({"error": "Post not found"}), 404

    comment = comments.get(comment_id)
    if comment is None:
        return json.dumps({"error": "Comment not found"}), 404

    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Bad Request"}), 400
    comment["text"] = text
    return json.dumps({
        "id": comment_id,
        "upvotes": comment["upvotes"],
        "text": text,
        "username": comment["username"]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
