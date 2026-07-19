"""Shared pytest fixtures for API contract tests."""
import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend = os.path.join(_root, "backend")
sys.path.insert(0, _root)
if os.path.isdir(_backend):
    sys.path.insert(0, _backend)

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest
from starlette.testclient import TestClient

import main


@pytest.fixture
def client():
    with TestClient(main.app) as c:
        yield c
