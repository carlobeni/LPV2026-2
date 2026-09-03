"""
test_api.py
Pruebas de integración para verificar los endpoints REST de FastAPI
y la generación del árbol nodal.
"""

from fastapi.testclient import TestClient
from main import app
from database import init_db
from init_db import populate_seed_data

client = TestClient(app)


def setup_module():
    init_db()
    populate_seed_data()


def test_get_stats_endpoint():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_commits" in data
    assert data["total_commits"] > 0


def test_get_commits_endpoint():
    response = client.get("/api/commits")
    assert response.status_code == 200
    commits = response.json()
    assert isinstance(commits, list)
    assert len(commits) > 0


def test_get_nodal_tree_endpoint():
    response = client.get("/api/nodal-tree")
    assert response.status_code == 200
    tree = response.json()
    assert isinstance(tree, list)
    # Verificar que el nodo raíz posee estructura con children
    assert "children" in tree[0]


def test_clear_database_endpoint():
    response = client.delete("/api/database")
    assert response.status_code == 200
    assert response.json()["message"] == "Base de datos vaciada exitosamente."

    stats_res = client.get("/api/stats")
    assert stats_res.json()["total_commits"] == 0

