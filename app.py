from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database to store tasks
tasks_db = []
task_id_counter = 1


# Helper function to find a task by its id
def find_task_by_id(task_id):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return None


# Helper function to generate a new task id
def generate_task_id():
    global task_id_counter
    new_id = task_id_counter
    task_id_counter += 1
    return new_id


# Endpoint to create a new task
@app.route("/v1/tasks", methods=["POST"])
def create_task():
    global tasks_db

    data = request.get_json()
    title = data.get("title", None)
    if title is None:
        return jsonify({"error": "Title is required"}), 400

    new_task = {"id": generate_task_id(), "title": title, "is_completed": False}
    tasks_db.append(new_task)

    return jsonify({"id": new_task["id"]}), 201


# Endpoint to list all tasks created
@app.route("/v1/tasks", methods=["GET"])
def list_tasks():
    return jsonify({"tasks": tasks_db}), 200


# Endpoint to get a specific task by id
@app.route("/v1/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "There is no task at that id"}), 404

    return jsonify(task), 200


# Endpoint to delete a specific task by id
@app.route("/v1/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks_db

    task = find_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "There is no task at that id"}), 404

    tasks_db = [task for task in tasks_db if task["id"] != task_id]
    return "", 204


# Endpoint to edit a specific task by id
@app.route("/v1/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    global tasks_db

    data = request.get_json()
    new_title = data.get("title", None)
    new_is_completed = data.get("is_completed", None)

    task = find_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "There is no task at that id"}), 404

    if new_title is not None:
        task["title"] = new_title

    if new_is_completed is not None:
        task["is_completed"] = new_is_completed

    return "", 204


# Extra Credit: Endpoint to bulk add tasks
@app.route("/v1/tasks/bulk", methods=["POST"])
def bulk_add_tasks():
    global tasks_db

    data = request.get_json()
    tasks_to_add = data.get("tasks", [])
    new_task_ids = []

    for task_info in tasks_to_add:
        title = task_info.get("title", None)
        if title is not None:
            new_task = {"id": generate_task_id(), "title": title, "is_completed": False}
            tasks_db.append(new_task)
            new_task_ids.append({"id": new_task["id"]})

    return jsonify({"tasks": new_task_ids}), 201


# Extra Credit: Endpoint to bulk delete tasks
@app.route("/v1/tasks/bulk", methods=["DELETE"])
def bulk_delete_tasks():
    global tasks_db

    data = request.get_json()
    tasks_to_delete = data.get("tasks", [])
    task_ids_to_delete = [task_info["id"] for task_info in tasks_to_delete]

    tasks_db = [task for task in tasks_db if task["id"] not in task_ids_to_delete]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
