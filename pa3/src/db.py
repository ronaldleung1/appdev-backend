import os
import sqlite3


# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Venmo app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect("venmo.db", check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.delete_transactions_table()
        self.delete_user_table()
        self.create_user_table()
        self.create_transactions_table()

    ### USERS

    def create_user_table(self):
        """
        Using SQL, create user table
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_user_table(self):
        """
        Using SQL, deletes user table
        """
        self.conn.execute("DROP TABLE IF EXISTS user;")

    def get_all_users(self):
        """
        Using SQL, get all users in the user table
        """
        cursor = self.conn.execute("SELECT * FROM user;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})

        return users

    def insert_user_table(self, name, username, balance=0):
        """
        Using SQL, adds a new user in the user table
        """
        cursor = self.conn.execute(
            "INSERT INTO user (name, username, balance) VALUES (?, ?, ?);",
            (name, username, balance),
        )
        self.conn.commit()

        return cursor.lastrowid

    def get_user_by_id(self, id):
        """
        Using SQL, get a user by ID
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE ID = ?;", (id,))

        for row in cursor:
            return {
                "id": row[0],
                "name": row[1],
                "username": row[2],
                "balance": int(row[3]),
                "transactions": self.get_transactions_of_user(id),
            }

        return None

    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user by id
        """
        self.conn.execute(
            """
            DELETE FROM user
            WHERE id = ?;
            """,
            (id,),
        )
        self.conn.commit()

    def send_money(self, sender_id, receiver_id, amount):
        """
        Using SQL, completes a transaction between the sender and receiver
        """
        # subtract from balance of sender
        self.conn.execute(
            """
            UPDATE user
            SET balance = balance - ?
            WHERE id = ?;
            """,
            (amount, sender_id),
        )

        # add to balance of receiver
        self.conn.execute(
            """
            UPDATE user
            SET balance = balance + ?
            WHERE id = ?;
            """,
            (amount, receiver_id),
        )
        self.conn.commit()

    ### TRANSACTIONS

    def create_transactions_table(self):
        """
        Using SQL, create transactions table
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    accepted BOOL,
                    FOREIGN KEY (sender_id) REFERENCES user(id),
                    FOREIGN KEY (receiver_id) REFERENCES user(id)
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_transactions_table(self):
        """
        Using SQL, delete transactions table
        """
        self.conn.execute("DROP TABLE IF EXISTS transactions;")

    def insert_transaction_table(
        self, timestamp, sender_id, receiver_id, amount, message, accepted=False
    ):
        """
        Using SQL, insert a transaction into the table
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions 
            (timestamp, sender_id, receiver_id, amount, message, accepted) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (timestamp, sender_id, receiver_id, amount, message, accepted),
        )
        self.conn.commit()

        return cursor.lastrowid

    def get_transaction_by_id(self, id):
        """
        Using SQL, get a transaction by ID
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE ID = ?;", (id,))

        for row in cursor:
            return {
                "id": int(row[0]),
                "timestamp": row[1],
                "sender_id": int(row[2]),
                "receiver_id": int(row[3]),
                "amount": int(row[4]),
                "message": row[5],
                "accepted": row[6],
            }

        return None

    def get_transactions_of_user(self, user_id):
        """
        Using SQL, get all transactions of a user
        """
        cursor = self.conn.execute(
            "SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?",
            (user_id, user_id),
        )
        transactions = []

        for row in cursor:
            transactions.append(
                {
                    "id": int(row[0]),
                    "timestamp": row[1],
                    "sender_id": int(row[2]),
                    "receiver_id": int(row[3]),
                    "amount": int(row[4]),
                    "message": row[5],
                    "accepted": row[6],
                }
            )

        return transactions

    def update_transaction_by_id(self, id, timestamp, accepted):
        """
        Using SQL, update a transaction by ID
        """
        cursor = self.conn.execute(
            """
            UPDATE transactions
            SET timestamp = ?, accepted = ?
            WHERE id = ?;
            """,
            (timestamp, accepted, id),
        )
        self.conn.commit()

        return cursor.lastrowid


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
