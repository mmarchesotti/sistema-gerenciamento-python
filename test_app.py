import unittest
import json
from app import app, init_db, DATABASE
import sqlite3

class TaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """
        Configuração inicial. Reinicializa o banco de dados e configura o cliente de teste.
        """
        init_db()

        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Testa se a rota principal retorna o template correto."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        """Testa a criação de uma nova tarefa."""
        data = {"title": "Teste Tarefa", "description": "Descrição da tarefa"}
        response = self.app.post(
            "/tasks",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Tarefa criada com sucesso!", response.get_json()["message"])
        self.assertIsInstance(response.get_json()["id"], int)

    def test_list_tasks(self):
        """Testa a listagem de tarefas."""
        self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )

        response = self.app.get("/tasks")
        self.assertEqual(response.status_code, 200)
        tasks = response.get_json()["tasks"]
    
        self.assertEqual(tasks[0]["title"], "Teste")

    def test_update_task(self):
        """Testa a atualização de uma tarefa existente."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        update_data = {"title": "Novo Título", "description": "Nova Descrição"}
        update_response = self.app.put(
            f"/tasks/{task_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertIn("Tarefa atualizada com sucesso!", update_response.get_json()["message"])

    def test_delete_task(self):
        """Testa a exclusão de uma tarefa."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        delete_response = self.app.delete(f"/tasks/{task_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("Tarefa excluída com sucesso!", delete_response.get_json()["message"])

    def test_set_completed(self):
        """Testa a atualização do status de 'completed'."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        update_data = {"completed": True}
        update_response = self.app.put(
            f"/setCompleted/{task_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertIn("Tarefa atualizada com sucesso!", update_response.get_json()["message"])

        list_response = self.app.get("/tasks")
        tasks = list_response.get_json()["tasks"]
        task = next(t for t in tasks if t["id"] == task_id)
        self.assertTrue(task["completed"])

if __name__ == "__main__":
    unittest.main()
