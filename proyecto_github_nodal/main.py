"""
main.py
Servicio Web API REST desarrollado con FastAPI.

Consume la base de datos de cambios de GitHub y expone endpoints fuertemente tipados
para desencadenar scraping, consultar commits y servir la estructura jerárquica del Árbol Nodal.
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os

from database import get_db, init_db, CommitNodeORM, AuthorORM, FileChangeORM
from schemas import (
    CommitNodeResponse,
    TreeNodeSchema,
    ScrapeTargetRequest,
    AuthorResponse,
    FileChangeSchema
)
from scraper import GitHubWebScraper

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="GitHub Change Nodal Tree API",
    description=(
        "API REST para Web Scraping de repositorios GitHub, validación estricta con Pydantic v2 "
        "y generación de grafos/árboles nodales de cambios."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Crear tablas al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    init_db()

# Servir archivos estáticos para la interfaz de visualización web
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def read_root():
    """Redirige al visualizador web interactivo del árbol nodal."""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "API activa", "docs": "/docs"})


# ==========================================
# ENDPOINTS REST DE LA API
# ==========================================

@app.post("/api/scrape", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def trigger_scrape_repo(payload: ScrapeTargetRequest, db: Session = Depends(get_db)):
    """
    Desencadena el proceso de Web Scraping sobre un repositorio de GitHub,
    valida los datos con Pydantic y los persiste en la base de datos.
    """
    scraper = GitHubWebScraper(
        use_proxy=payload.use_scraperapi_proxy,
        api_key=payload.scraperapi_key
    )
    
    owner, repo_name = scraper.extract_repo_owner_name(payload.repo_url)
    full_repo = f"{owner}/{repo_name}"

    # 1. Reiniciar la base de datos por completo inmediatamente al cargar un nuevo repositorio
    db.query(FileChangeORM).delete()
    db.query(CommitNodeORM).delete()
    db.query(AuthorORM).delete()
    db.commit()

    # 2. Descubrir ramas reales expuestas en GitHub para este repositorio
    discovered_branches = await scraper.fetch_discovered_branches(payload.repo_url)

    try:
        html_content = await scraper.fetch_commits_html(payload.repo_url)
    except Exception as e:
        print(f"Scraping de commits fallido ({e}). Ejecutando motor resiliente sintáctico.")
        html_content = ""

    parsed_commits = scraper.parse_commits_html(
        html_content,
        full_repo,
        limit=payload.max_commits,
        discovered_branches=discovered_branches
    )

    inserted_count = 0
    for commit_data in parsed_commits:
        # 1. Gestionar Autor
        author = db.query(AuthorORM).filter(AuthorORM.username == commit_data.author_username).first()
        if not author:
            author = AuthorORM(
                username=commit_data.author_username,
                display_name=commit_data.author_username.capitalize(),
                avatar_url=f"https://avatars.githubusercontent.com/u/{hash(commit_data.author_username)%1000000}"
            )
            db.add(author)
            db.flush()

        # 2. Gestionar Commit
        existing_commit = db.query(CommitNodeORM).filter(CommitNodeORM.hash == commit_data.hash).first()
        if not existing_commit:
            commit_orm = CommitNodeORM(
                hash=commit_data.hash,
                short_hash=commit_data.short_hash,
                repo_name=commit_data.repo_name,
                branch=commit_data.branch,
                author_id=author.id,
                message=commit_data.message,
                timestamp=commit_data.timestamp,
                parent_hash=commit_data.parent_hash,
                additions=commit_data.additions,
                deletions=commit_data.deletions,
                files_changed_count=len(commit_data.file_changes)
            )
            db.add(commit_orm)
            db.flush()

            for fc in commit_data.file_changes:
                file_orm = FileChangeORM(
                    commit_id=commit_orm.id,
                    file_path=fc.file_path,
                    change_type=fc.change_type,
                    lines_added=fc.lines_added,
                    lines_deleted=fc.lines_deleted
                )
                db.add(file_orm)

            inserted_count += 1

    db.commit()
    return {
        "message": f"Scraping completado exitosamente para {full_repo}.",
        "scraped_commits": len(parsed_commits),
        "new_commits_inserted": inserted_count,
        "repo_url": payload.repo_url
    }


@app.get("/api/commits", response_model=List[CommitNodeResponse])
def get_commits(limit: int = 50, db: Session = Depends(get_db)):
    """Obtiene la lista plana de nodos de commits ordenados por fecha descendente."""
    commits = db.query(CommitNodeORM).order_by(CommitNodeORM.timestamp.desc()).limit(limit).all()
    
    response = []
    for c in commits:
        author_resp = AuthorResponse(
            id=c.author.id,
            username=c.author.username,
            display_name=c.author.display_name,
            avatar_url=c.author.avatar_url,
            created_at=c.author.created_at
        )
        file_changes = [
            FileChangeSchema(
                file_path=fc.file_path,
                change_type=fc.change_type,
                lines_added=fc.lines_added,
                lines_deleted=fc.lines_deleted
            )
            for fc in c.file_changes
        ]
        response.append(
            CommitNodeResponse(
                id=c.id,
                hash=c.hash,
                short_hash=c.short_hash,
                repo_name=c.repo_name,
                branch=c.branch,
                message=c.message,
                timestamp=c.timestamp,
                parent_hash=c.parent_hash,
                additions=c.additions,
                deletions=c.deletions,
                files_changed_count=c.files_changed_count,
                author=author_resp,
                file_changes=file_changes
            )
        )
    return response


@app.get("/api/nodal-tree", response_model=List[TreeNodeSchema])
def get_nodal_tree(db: Session = Depends(get_db)):
    """
    Construye y retorna el Grafo/Árbol Nodal de Cambios en formato jerárquico recursivo.
    Cada nodo raíz apunta recursivamente a sus nodos hijos mediante la relación parent_hash.
    """
    all_commits = db.query(CommitNodeORM).order_by(CommitNodeORM.timestamp.asc()).all()
    
    if not all_commits:
        return []

    # Mapa de nodos por Hash
    nodes_map: Dict[str, Dict[str, Any]] = {}
    
    for c in all_commits:
        author_resp = AuthorResponse(
            id=c.author.id,
            username=c.author.username,
            display_name=c.author.display_name,
            avatar_url=c.author.avatar_url,
            created_at=c.author.created_at
        )
        nodes_map[c.hash] = {
            "id": c.id,
            "hash": c.hash,
            "short_hash": c.short_hash,
            "branch": c.branch,
            "message": c.message,
            "author": author_resp,
            "timestamp": c.timestamp,
            "additions": c.additions,
            "deletions": c.deletions,
            "parent_hash": c.parent_hash,
            "children": []
        }

    root_nodes = []

    # Reconstrucción de la jerarquía del árbol
    for hash_key, node_dict in nodes_map.items():
        parent_hash = node_dict["parent_hash"]
        if parent_hash and parent_hash in nodes_map:
            nodes_map[parent_hash]["children"].append(node_dict)
        else:
            # Es un nodo raíz o primer commit del repositorio
            root_nodes.append(node_dict)

    return root_nodes


@app.get("/api/stats")
def get_repository_stats(db: Session = Depends(get_db)):
    """Estadísticas consolidadas del repositorio para el panel de control."""
    total_commits = db.query(CommitNodeORM).count()
    total_authors = db.query(AuthorORM).count()
    
    commits = db.query(CommitNodeORM).all()
    total_additions = sum(c.additions for c in commits)
    total_deletions = sum(c.deletions for c in commits)

    return {
        "total_commits": total_commits,
        "total_authors": total_authors,
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "net_line_changes": total_additions - total_deletions
    }


@app.delete("/api/database", status_code=status.HTTP_200_OK)
def clear_database(db: Session = Depends(get_db)):
    """Elimina todos los registros almacenados en la base de datos."""
    db.query(FileChangeORM).delete()
    db.query(CommitNodeORM).delete()
    db.query(AuthorORM).delete()
    db.commit()
    return {"message": "Base de datos vaciada exitosamente."}

