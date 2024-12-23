from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'tasks.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        task_id = cursor.lastrowid
        conn.commit()
        return jsonify({ "message": "Tarefa criada com sucesso!", "id": task_id}), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = [
            {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}
            for row in cursor.fetchall()
        ]
        return jsonify({"message": "Dados recuperados com sucesso", "tasks": tasks})


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
            (title, description, task_id)
        )
        conn.commit()
        return jsonify({"message": "Tarefa atualizada com sucesso!"})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return jsonify({"message": "Tarefa excluída com sucesso!"})


@app.route("/setCompleted/<int:task_id>", methods=["PUT"])
def setCompleted(task_id):
    data = request.get_json()
    completed = data.get("completed")

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (completed, task_id)
        )
        conn.commit()
        return jsonify({"message": "Tarefa atualizada com sucesso!"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
