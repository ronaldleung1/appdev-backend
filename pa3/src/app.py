import json
from flask import Flask, request
import db
from datetime import datetime

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


### USERS


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


### TRANSACTIONS


@app.route("/api/transactions/", methods=["POST"])
def create_transaction():
    """
    Endpoint for creating transactions by sending or requesting money
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    message = body.get("message")
    accepted = body.get("accepted")

    if (
        sender_id is not None
        and receiver_id is not None
        and amount is not None
        and message is not None
    ):
        sender = DB.get_user_by_id(sender_id)
        receiver = DB.get_user_by_id(receiver_id)

        if sender is None or receiver is None:
            return json.dumps({"error": "User not found"}), 404

        # if accepted is true, update the balances if sender has sufficient funds
        if accepted:
            if amount > sender["balance"]:
                return (
                    json.dumps(
                        {"error": "Forbidden: Sender does not have enough money"}
                    ),
                    403,
                )
            DB.send_money(sender_id, receiver_id, amount)

        # record the transaction in database
        transaction_id = DB.insert_transaction_table(
            datetime.now(), sender_id, receiver_id, amount, message, accepted
        )
        transaction = DB.get_transaction_by_id(transaction_id)

        if transaction is None:
            return (
                json.dumps({"error": "Something went wrong while making transaction"}),
                400,
            )

        return json.dumps(transaction), 201

    return json.dumps({"error": "Insufficient or incorrect arguments provided"}), 400


@app.route("/api/transactions/<int:transaction_id>/", methods=["POST"])
def manage_payment_request(transaction_id):
    """
    Endpoint for accepting or denying a payment request
    """
    body = json.loads(request.data)
    accepted = body.get("accepted")

    if accepted is not None:
        transaction = DB.get_transaction_by_id(transaction_id)

        if transaction is None:
            return json.dumps({"error": "Transaction not found"}), 404

        if transaction["accepted"] is None:
            if accepted:
                # If sender does not have enough money in their balance, return an error response
                sender = DB.get_user_by_id(transaction["sender_id"])
                if transaction["amount"] > sender["balance"]:
                    return (
                        json.dumps(
                            {"error": "Forbidden: Sender does not have enough money"}
                        ),
                        403,
                    )

                DB.update_transaction_by_id(
                    transaction_id, datetime.now(), True
                )  # accepted will always be true
                DB.send_money(
                    transaction["sender_id"],
                    transaction["receiver_id"],
                    transaction["amount"],
                )
            else:
                DB.update_transaction_by_id(
                    transaction_id, datetime.now(), False
                )  # accepted will always be false

            # get updated transaction and return it
            transaction = DB.get_transaction_by_id(transaction_id)
            if transaction is None:
                return (
                    json.dumps(
                        {"error": "Something went wrong while managing payment request"}
                    ),
                    400,
                )

            return json.dumps(transaction), 200

        return (
            json.dumps(
                {
                    "error": "Forbidden: Cannot change accepted field if transaction has already been accepted or denied"
                }
            ),
            403,
        )

    return json.dumps({"error": "Insufficient or incorrect arguments provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
