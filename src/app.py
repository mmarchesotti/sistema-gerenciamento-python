from flask import Flask, request, jsonify
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
    return "Bem-vindo ao sistema de gerenciamento de tarefas!"

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
        conn.commit()
        return jsonify({"message": "Tarefa criada com sucesso!"}), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = [
            {"id": row[0], "title": row[1], "description": row[2], "completed": bool(row[3])}
            for row in cursor.fetchall()
        ]
        return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
            (title, description, completed, task_id)
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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
