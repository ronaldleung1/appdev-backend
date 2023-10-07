from flask import Flask, request
import json

app = Flask(__name__)

tasks = {
    0: {'id': 1, "description": "Do Laundry","done": False},
    1: {'id': 2, "description": "Do Homework","done": False}
}

task_current_id = 2

# GET tasks
@app.route('/tasks/')
def get_tasks():
    """
    Get all the tasks
    """
    res = {"tasks": list(tasks.values())}
    return json.dumps(res), 200

# POST task

@app.route('/tasks/', methods=["POST"])
def create_tasks():
    """
    Creates a task
    """
    global task_current_id
    body = json.loads(request.data)
    description = body.get("description")
    task_current_id += 1
    task = {"id": task_current_id, "description": description, "done": False}
    tasks[task_current_id] = task
    return json.dumps(task), 201

@app.route('/tasks/<int:task_id>/')
def get_one_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>/", methods=["PUT"])
def update_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404
    body = json.loads(request.data)
    task["done"] = body.get("done")
    return json.dumps(task), 200

@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404
    del tasks[task_id]
    return json.dumps(task), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
