"""
database.py
Módulo de persistencia independiente para el registro de cambios de repositorios GitHub.
Administra la conexión a SQLite en modo WAL (Write-Ahead Logging) y la definición de tablas ORM.
"""

from datetime import datetime
from typing import Generator
import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

DB_PATH = os.getenv("DATABASE_PATH", "github_nodal.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Motor SQLite optimizado con WAL para accesos concurrentes de scraping y API REST
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class AuthorORM(Base):
    """Representa a un desarrollador/usuario que realiza cambios en el repositorio."""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(150), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    commits = relationship("CommitNodeORM", back_populates="author")


class CommitNodeORM(Base):
    """
    Representa un nodo de cambio (Commit) en la estructura arborescente.
    Incluye punteros al nodo padre (parent_hash) para reconstruir el árbol nodal.
    """
    __tablename__ = "commit_nodes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hash = Column(String(40), unique=True, index=True, nullable=False)
    short_hash = Column(String(10), nullable=False)
    repo_name = Column(String(150), index=True, nullable=False)
    branch = Column(String(100), default="main", nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    parent_hash = Column(String(40), nullable=True, index=True)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    files_changed_count = Column(Integer, default=0)

    author = relationship("AuthorORM", back_populates="commits")
    file_changes = relationship("FileChangeORM", back_populates="commit", cascade="all, delete-orphan")


class FileChangeORM(Base):
    """Detalle de archivo individual modificado dentro de un commit."""
    __tablename__ = "file_changes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    commit_id = Column(Integer, ForeignKey("commit_nodes.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    change_type = Column(String(20), default="MODIFIED")  # ADDED, MODIFIED, DELETED
    lines_added = Column(Integer, default=0)
    lines_deleted = Column(Integer, default=0)

    commit = relationship("CommitNodeORM", back_populates="file_changes")


def init_db():
    """Inicializa la base de datos creando todas las tablas definidas."""
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        # Habilitar modo WAL para SQLite
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
    print("Base de datos 'github_nodal.db' inicializada correctamente.")


def get_db() -> Generator[Session, None, None]:
    """Inyector de dependencia para FastAPI para gestionar la sesión de BD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
