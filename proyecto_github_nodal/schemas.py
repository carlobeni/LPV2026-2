"""
schemas.py
Modelos de datos y validación estricta con Pydantic v2.

Soluciona la problemática del tipado dinámico en Python garantizando que:
1. El parsing del HTML scrapeado convierta texto crudo a tipos nativos validados.
2. La API REST rechace cargas malformadas y responda con estructuras fuertemente tipadas.
3. El árbol nodal de cambios mantenga integridad referencial en formato de grafo arborescente.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator, ConfigDict


# ==========================================
# 1. MODELOS DE AUTORES Y CAMBIOS DE ARCHIVO
# ==========================================

class AuthorBase(BaseModel):
    """Esquema base para un usuario/colaborador de GitHub."""
    username: str = Field(..., min_length=1, max_length=100, description="Nombre de usuario de GitHub")
    display_name: Optional[str] = Field(None, max_length=150, description="Nombre completo o visible")
    avatar_url: Optional[str] = Field(None, description="URL del avatar del autor")

    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str) -> str:
        """Saneamiento de nombres de usuario scrapeados de HTML."""
        return v.strip().lstrip("@")


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileChangeSchema(BaseModel):
    """Representa la modificación de un archivo individual en un commit."""
    file_path: str = Field(..., description="Ruta relativa del archivo en el repositorio")
    change_type: str = Field("MODIFIED", description="Tipo de cambio: ADDED, MODIFIED, DELETED")
    lines_added: int = Field(0, ge=0, description="Líneas insertadas (+)")
    lines_deleted: int = Field(0, ge=0, description="Líneas eliminadas (-)")

    @field_validator("change_type")
    @classmethod
    def validate_change_type(cls, v: str) -> str:
        v_upper = v.upper().strip()
        if v_upper not in ["ADDED", "MODIFIED", "DELETED", "RENAMED"]:
            return "MODIFIED"
        return v_upper


# ==========================================
# 2. MODELOS DE COMMITS Y NODOS DE CAMBIOS
# ==========================================

class CommitNodeBase(BaseModel):
    """
    Nodo individual de la cadena/árbol de cambios.
    Representa un commit realizado por un desarrollador.
    """
    hash: str = Field(..., min_length=7, max_length=40, description="Hash SHA-1 del commit")
    short_hash: Optional[str] = Field(None, description="Hash abreviado a 7 caracteres")
    repo_name: str = Field(..., description="Nombre del repositorio en formato 'usuario/repo'")
    branch: str = Field("main", description="Rama donde se aplicó el cambio")
    message: str = Field(..., min_length=1, description="Mensaje del commit")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora UTC del cambio")
    parent_hash: Optional[str] = Field(None, description="SHA-1 del commit padre (conecta los nodos del árbol)")
    additions: int = Field(0, ge=0)
    deletions: int = Field(0, ge=0)

    @field_validator("hash")
    @classmethod
    def validate_hash_format(cls, v: str) -> str:
        clean_v = v.strip().lower()
        if not clean_v.isalnum():
            raise ValueError("El Hash del commit debe contener únicamente caracteres alfanuméricos.")
        return clean_v

    @model_validator(mode="after")
    def populate_short_hash(self) -> "CommitNodeBase":
        if not self.short_hash and self.hash:
            self.short_hash = self.hash[:7]
        return self


class CommitNodeCreate(CommitNodeBase):
    author_username: str
    file_changes: List[FileChangeSchema] = []


class CommitNodeResponse(CommitNodeBase):
    id: int
    author: AuthorResponse
    file_changes: List[FileChangeSchema] = []
    files_changed_count: int = 0

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. ESTRUCTURA RECURSIVA PARA EL ÁRBOL NODAL
# ==========================================

class TreeNodeSchema(BaseModel):
    """
    Estructura jerárquica nodal de cambios.
    Cada nodo contiene los datos del commit y una lista recursiva de nodos hijos.
    """
    id: int
    hash: str
    short_hash: str
    message: str
    author: AuthorResponse
    timestamp: datetime
    additions: int
    deletions: int
    parent_hash: Optional[str] = None
    children: List["TreeNodeSchema"] = []

    model_config = ConfigDict(from_attributes=True)


# Permitir auto-referencia recursiva en Pydantic v2
TreeNodeSchema.model_rebuild()


# ==========================================
# 4. SOLICITUD DE SCRAPING DE REPOSITORIO
# ==========================================

class ScrapeTargetRequest(BaseModel):
    """Solicitud POST para ejecutar el scraping de un repositorio específico de GitHub."""
    repo_url: str = Field(..., example="https://github.com/fastapi/fastapi", description="URL completa del repositorio GitHub")
    max_commits: int = Field(15, ge=1, le=50, description="Límite de commits a scrapear y analizar")
    use_scraperapi_proxy: bool = Field(False, description="Indica si debe enrutar las peticiones por ScraperAPI / Proxies")
    scraperapi_key: Optional[str] = Field(None, description="API Key de ScraperAPI si está activo el proxy")

    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        v_clean = v.strip().rstrip("/")
        if "github.com" not in v_clean:
            raise ValueError("La URL debe pertenecer al dominio 'github.com'.")
        return v_clean
