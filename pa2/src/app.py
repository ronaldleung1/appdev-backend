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


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting a user
    """
    
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    return json.dumps(user), 200


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user
    """
    
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Endpoint for sending money between users
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")

    if sender_id is not None and receiver_id is not None and amount is not None:
        sender = DB.get_user_by_id(sender_id)
        receiver = DB.get_user_by_id(receiver_id)
        if sender is None or receiver is None:
            return json.dumps({"error": "Sender not found"}), 404
        
        if amount > sender["balance"]:
            return json.dumps({"error": "Sender does not have enough money"}), 400
    
        DB.send_money(sender_id, receiver_id, amount)
        
        return json.dumps({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount
        }), 200
    
    return json.dumps({"error": "Insufficient or incorrect arguments provided"}), 400
  
  
  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
