import pytest
from unittest.mock import MagicMock, patch
import shutil
import os
from pathlib import Path
import json


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Cleanup __pycache__ and unwanted local Ansible collections after tests."""
    yield  # Run tests first, then cleanup after session.

    # Define paths to clean
    project_root = Path(__file__).resolve().parents[1]
    collections_path = project_root / "collections"

    # Remove all __pycache__ directories
    for pycache in project_root.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            print(f"Removed: {pycache}")
        except Exception as e:
            print(f"Could not remove {pycache}: {e}")

    # Remove local Ansible collections folder if it exists
    if collections_path.exists():
        try:
            shutil.rmtree(collections_path)
            print(f"Removed local collections folder: {collections_path}")
        except Exception as e:
            print(f"Could not remove {collections_path}: {e}")