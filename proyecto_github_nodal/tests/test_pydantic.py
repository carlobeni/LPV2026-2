"""
test_pydantic.py
Pruebas unitarias para verificar los modelos de Pydantic v2,
coerción de tipos y validadores personalizados.
"""

import pytest
from pydantic import ValidationError
from schemas import CommitNodeCreate, AuthorCreate, ScrapeTargetRequest


def test_author_schema_validation():
    author = AuthorCreate(username=" @tiangolo ")
    assert author.username == "tiangolo"


def test_commit_node_validation_and_coercion():
    commit = CommitNodeCreate(
        hash="A1B2C3D4E5F67890123456789012345678901234",
        repo_name="fastapi/fastapi",
        branch="main",
        message="Initial commit",
        additions=150,
        deletions=10,
        author_username="tiangolo"
    )
    assert commit.hash == "a1b2c3d4e5f67890123456789012345678901234"
    assert commit.short_hash == "a1b2c3d"


def test_scrape_target_request_invalid_url():
    with pytest.raises(ValidationError):
        ScrapeTargetRequest(repo_url="https://invalid-domain.com/repo")
