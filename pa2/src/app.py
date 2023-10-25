import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/users/", methods=["GET"])
def get_users():
    """
    Endpoint for getting all users
    """
    res = {"users": DB.get_all_users()}
    return json.dumps(res), 200

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    print("balance: " + str(balance))
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "Something went wrong while making user"}), 400
    return json.dumps(user), 201




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
