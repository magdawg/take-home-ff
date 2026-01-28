"""Shared test fixtures and configuration"""

import sys
from pathlib import Path

import pytest

# Add project root to path so we can import backend package
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.src.storage import clear_assets


@pytest.fixture(autouse=True)
def clear_assets_store():
    """Clear assets store before each test"""
    clear_assets()
    yield
    clear_assets()
