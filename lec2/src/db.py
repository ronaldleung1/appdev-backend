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
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and stores it in an instance variable
        """
        
        self.conn = sqlite3.connect(
            "todo.db", check_same_thread=False
        )

        # self.delete_task_table()
        self.create_task_table()

    def create_task_table(self):
        """
        Using SQL, create task table
        """

        try:
            self.conn.execute(
                """
                CREATE TABLE task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_task_table(self):
        """
        Using SQL, deletes task table
        """

        self.conn.execute("DROP TABLE IF EXISTS task;")
    
    def get_all_tasks(self):
        """
        Using SQL, get all tasks in the task table
        """
        cursor = self.conn.execute("SELECT * FROM task;")
        tasks = []

        for row in cursor:
            tasks.append({"id": row[0], "description": row[1], "done": bool(row[2])})
        
        return tasks
    
    def insert_task_table(self, description, done):
        """
        Using SQL, adds a new taks in the task table
        """
        cursor = self.conn.execute("INSERT INTO task (description, done) VALUES (?, ?);", (description, done))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_task_by_id(self, id):
        """
        Using SQL, get a task by ID
        """
        cursor = self.conn.execute("SELECT * FROM task WHERE ID = ?;", (id,))

        for row in cursor:
            return({"id": row[0], "description": row[1], "done": bool(row[2])})

        return None
    
    def update_task_by_id(self, id, description, done):
        """
        Using SQL, update a task by ID
        """
        
        self.conn.execute(
            """
            UPDATE task
            SET description = ?, done = ?
            WHERE id = ?;
            """,
            (description, done, id)
        )
        self.conn.commit()
    
    def delete_task_by_id(self, id):
        """
        Using SQL, deletes a task by id
        """

        self.conn.execute(
            """
            DELETE FROM task
            WHERE id = ?;
            """,
            (id,)
        )
        self.conn.commit()

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
