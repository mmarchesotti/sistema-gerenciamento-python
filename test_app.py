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
    
        self.assertEqual(tasks[-1]["title"], "Teste")

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


    def test_create_task_missing_title(self):
        """Testa a criação de tarefa sem título."""
        data = {"description": "Descrição da tarefa"}
        response = self.app.post(
            "/tasks",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)


    def test_create_task_empty_description(self):
        """Testa a criação de uma tarefa com descrição vazia."""
        data = {"title": "Tarefa sem descrição", "description": ""}
        response = self.app.post(
            "/tasks",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Tarefa criada com sucesso!", response.get_json()["message"])


    def test_update_non_existing_task(self):
        """Testa a atualização de uma tarefa que não existe."""
        update_data = {"title": "Novo Título", "description": "Nova Descrição"}
        response = self.app.put(
            "/tasks/99999",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


    def test_delete_non_existing_task(self):
        """Testa a exclusão de uma tarefa que não existe."""
        response = self.app.delete("/tasks/99999")
        self.assertEqual(response.status_code, 200)


    def test_set_completed_missing_field(self):
        """Testa a atualização do status 'completed' sem o campo especificado."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        response = self.app.put(
            f"/setCompleted/{task_id}",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


    def test_update_task_empty_description(self):
        """Testa a atualização da descrição para uma descrição vazia."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        update_data = {"title": "Novo título", "description": ""}
        update_response = self.app.put(
            f"/tasks/{task_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(update_response.status_code, 200)


    def test_set_completed_false(self):
        """Testa a atualização do status de 'completed' para False."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        update_data = {"completed": False}
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
        self.assertFalse(task["completed"])


    def test_list_tasks_after_deletion(self):
        """Testa a listagem de tarefas após a exclusão."""
        create_response = self.app.post(
            "/tasks",
            data=json.dumps({"title": "Teste", "description": "Descrição"}),
            content_type="application/json"
        )
        task_id = create_response.get_json()["id"]

        delete_response = self.app.delete(f"/tasks/{task_id}")
        self.assertEqual(delete_response.status_code, 200)

        list_response = self.app.get("/tasks")
        tasks = list_response.get_json()["tasks"]
        self.assertNotIn(task_id, [task["id"] for task in tasks])


    def test_create_task_long_description(self):
        """Testa a criação de tarefa com descrição longa."""
        long_description = "A" * 1000
        data = {"title": "Tarefa Longa", "description": long_description}
        response = self.app.post(
            "/tasks",
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
