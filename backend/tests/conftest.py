"""Shared test fixtures and configuration"""

import sys
from pathlib import Path

import pytest

from backend.src.storage import clear_assets


@pytest.fixture(autouse=True)
def clear_assets_store():
    """Clear assets store before each test"""
    clear_assets()
    yield
    clear_assets()
