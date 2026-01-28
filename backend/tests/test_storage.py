"""Tests for storage module"""

import pytest

from backend.src.models import AssetData
from backend.src.storage import (
    asset_count,
    clear_assets,
    get_all_assets,
    get_asset,
    store_asset,
)


class TestStorage:
    """Test in-memory storage functions"""

    def test_store_asset(self):
        """Test storing an asset"""
        data = AssetData(
            id="id-1",
            nominal_value=100,
            due_date="2025-12-04",
            interest_rate=0.05,
        )
        store_asset("id-1", data)
        assert get_asset("id-1") == data

    def test_get_all_assets(self):
        """Test retrieving all assets"""
        asset1 = AssetData(
            id="id-1",
            nominal_value=100,
            due_date="2025-12-04",
            interest_rate=0.05,
        )
        asset2 = AssetData(
            id="id-2",
            nominal_value=50,
            due_date="2025-12-04",
            interest_rate=0.03,
        )
        store_asset("id-1", asset1)
        store_asset("id-2", asset2)

        all_assets = get_all_assets()
        assert len(all_assets) == 2

    def test_get_asset_not_found(self):
        """Test getting non-existent asset"""
        result = get_asset("non-existent")
        assert result is None

    def test_clear_assets(self):
        """Test clearing all assets"""
        store_asset(
            "id-1",
            AssetData(
                id="id-1", nominal_value=100, due_date="2025-12-04", interest_rate=0.05
            ),
        )
        assert asset_count() == 1

        clear_assets()
        assert asset_count() == 0

    def test_asset_count(self):
        """Test counting assets"""
        assert asset_count() == 0

        store_asset(
            "id-1",
            AssetData(
                id="id-1", nominal_value=100, due_date="2025-12-04", interest_rate=0.05
            ),
        )
        assert asset_count() == 1

        store_asset(
            "id-2",
            AssetData(
                id="id-2", nominal_value=50, due_date="2025-12-04", interest_rate=0.03
            ),
        )
        assert asset_count() == 2

    def test_update_asset(self):
        """Test updating existing asset"""
        data1 = AssetData(
            id="id-1", nominal_value=100, due_date="2025-12-04", interest_rate=0.05
        )
        data2 = AssetData(
            id="id-1", nominal_value=200, due_date="2025-12-04", interest_rate=0.05
        )

        store_asset("id-1", data1)
        assert get_asset("id-1").nominal_value == 100

        store_asset("id-1", data2)
        assert get_asset("id-1").nominal_value == 200
