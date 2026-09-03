"""
init_db.py
Script independiente para desplegar la base de datos local/remota de forma desacoplada a la API REST.
Puede ejecutarse directamente desde la consola: `python init_db.py`
"""

from datetime import datetime, timedelta
import random
from database import init_db, SessionLocal, AuthorORM, CommitNodeORM, FileChangeORM


def populate_seed_data():
    """Genera datos semilla iniciales para verificar el grafo nodal de cambios."""
    db = SessionLocal()
    try:
        # Verificar si ya existen registros
        if db.query(CommitNodeORM).first():
            print("La base de datos ya posee registros. Omitiendo seed inicial.")
            return

        print("Insertando historial nodal de cambios de prueba (Seed Data)...")

        # 1. Autores
        authors_data = [
            {"username": "tiangolo", "display_name": "Sebastián Ramírez", "avatar_url": "https://avatars.githubusercontent.com/u/1326112"},
            {"username": "tomchristie", "display_name": "Tom Christie", "avatar_url": "https://avatars.githubusercontent.com/u/647359"},
            {"username": "samuelcolvin", "display_name": "Samuel Colvin", "avatar_url": "https://avatars.githubusercontent.com/u/4041185"},
            {"username": "carlosbenitez", "display_name": "Carlos Benítez", "avatar_url": "https://avatars.githubusercontent.com/u/1000000"}
        ]

        author_objs = {}
        for a_data in authors_data:
            author = AuthorORM(**a_data)
            db.add(author)
            db.flush()
            author_objs[a_data["username"]] = author

        # 2. Árbol Nodal de Commits (Secuencia de Hash y Padres)
        commits_tree = [
            {
                "hash": "a1b2c3d4e5f67890123456789012345678901234",
                "short_hash": "a1b2c3d",
                "repo_name": "fastapi/fastapi",
                "branch": "main",
                "author": "tiangolo",
                "message": "Initial commit: Core ASGI router and Pydantic OpenAPI schemas engine",
                "timestamp": datetime.utcnow() - timedelta(days=10),
                "parent_hash": None,
                "additions": 450,
                "deletions": 0,
                "files": [
                    ("fastapi/__init__.py", "ADDED", 50, 0),
                    ("fastapi/applications.py", "ADDED", 250, 0),
                    ("fastapi/routing.py", "ADDED", 150, 0)
                ]
            },
            {
                "hash": "b2c3d4e5f67890123456789012345678901234a5",
                "short_hash": "b2c3d4e",
                "repo_name": "fastapi/fastapi",
                "branch": "main",
                "author": "samuelcolvin",
                "message": "Feat: Integrate Pydantic v2 core rust parser for payload validation",
                "timestamp": datetime.utcnow() - timedelta(days=8),
                "parent_hash": "a1b2c3d4e5f67890123456789012345678901234",
                "additions": 180,
                "deletions": 40,
                "files": [
                    ("fastapi/datatypes.py", "ADDED", 100, 0),
                    ("fastapi/routing.py", "MODIFIED", 80, 40)
                ]
            },
            {
                "hash": "c3d4e5f67890123456789012345678901234a5b6",
                "short_hash": "c3d4e5f",
                "repo_name": "fastapi/fastapi",
                "branch": "main",
                "author": "tomchristie",
                "message": "Refactor: Starlette HTTP response handlers and streaming endpoints",
                "timestamp": datetime.utcnow() - timedelta(days=5),
                "parent_hash": "b2c3d4e5f67890123456789012345678901234a5",
                "additions": 95,
                "deletions": 15,
                "files": [
                    ("fastapi/responses.py", "MODIFIED", 95, 15)
                ]
            },
            {
                "hash": "d4e5f67890123456789012345678901234a5b6c7",
                "short_hash": "d4e5f67",
                "repo_name": "fastapi/fastapi",
                "branch": "main",
                "author": "carlosbenitez",
                "message": "Fix: Handle custom Pydantic ValidationError in global exception handlers",
                "timestamp": datetime.utcnow() - timedelta(days=2),
                "parent_hash": "c3d4e5f67890123456789012345678901234a5b6",
                "additions": 64,
                "deletions": 8,
                "files": [
                    ("fastapi/exceptions.py", "ADDED", 44, 0),
                    ("fastapi/applications.py", "MODIFIED", 20, 8)
                ]
            },
            {
                "hash": "e5f67890123456789012345678901234a5b6c7d8",
                "short_hash": "e5f6789",
                "repo_name": "fastapi/fastapi",
                "branch": "main",
                "author": "tiangolo",
                "message": "Docs: Add visual nodal graph documentation and OpenAPI 3.1 updates",
                "timestamp": datetime.utcnow() - timedelta(hours=6),
                "parent_hash": "d4e5f67890123456789012345678901234a5b6c7",
                "additions": 120,
                "deletions": 5,
                "files": [
                    ("docs/index.md", "MODIFIED", 120, 5)
                ]
            }
        ]

        for c_data in commits_tree:
            author_obj = author_objs[c_data["author"]]
            commit = CommitNodeORM(
                hash=c_data["hash"],
                short_hash=c_data["short_hash"],
                repo_name=c_data["repo_name"],
                branch=c_data["branch"],
                author_id=author_obj.id,
                message=c_data["message"],
                timestamp=c_data["timestamp"],
                parent_hash=c_data["parent_hash"],
                additions=c_data["additions"],
                deletions=c_data["deletions"],
                files_changed_count=len(c_data["files"])
            )
            db.add(commit)
            db.flush()

            for path, ctype, add_l, del_l in c_data["files"]:
                file_change = FileChangeORM(
                    commit_id=commit.id,
                    file_path=path,
                    change_type=ctype,
                    lines_added=add_l,
                    lines_deleted=del_l
                )
                db.add(file_change)

        db.commit()
        print("Semilla de base de datos cargada exitosamente.")
    except Exception as e:
        db.rollback()
        print(f"Error al poblar base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("--- Inicializador Independiente de Servidor de Base de Datos ---")
    init_db()
    populate_seed_data()
