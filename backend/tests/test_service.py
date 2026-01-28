"""Tests for service module business logic"""

from datetime import UTC, datetime, timedelta

import pytest

from backend.src.models import AssetData, AssetInput
from backend.src.service import (
    calculate_insights,
    determine_asset_status,
    prepare_asset_output,
    validate_assets_input,
)
from backend.src.storage import clear_assets, store_asset


class TestAssetStatus:
    """Test asset status determination"""

    def test_active_asset(self):
        """Test active asset (future due date)"""
        future_date = (datetime.now(UTC) + timedelta(days=365)).strftime("%Y-%m-%d")
        status = determine_asset_status(future_date)
        assert status == "active"

    def test_defaulted_asset(self):
        """Test defaulted asset (past due date)"""
        past_date = (datetime.now(UTC) - timedelta(days=10)).strftime("%Y-%m-%d")
        status = determine_asset_status(past_date)
        assert status == "defaulted"

    def test_invalid_date_format(self):
        """Test invalid date format raises error"""
        with pytest.raises(ValueError, match="Invalid date format"):
            determine_asset_status("2025/12/04")

    def test_edge_case_today(self):
        """Test asset due today is active"""
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        status = determine_asset_status(today)
        # Today is not in the past, so it should be active
        assert status == "active"


class TestValidation:
    """Test input validation"""

    def test_valid_asset_input(self):
        """Test valid asset input passes validation"""
        assets = [
            AssetInput(
                id="id-1",
                nominal_value=100,
                due_date="2025-12-04",
                interest_rate=0.05,
            )
        ]
        # Should not raise
        validate_assets_input(assets)

    def test_negative_nominal_value(self):
        """Test negative nominal value raises error"""
        assets = [
            AssetInput(
                id="id-1",
                nominal_value=-100,
                due_date="2025-12-04",
                interest_rate=0.05,
            )
        ]
        with pytest.raises(ValueError, match="negative nominal_value"):
            validate_assets_input(assets)

    def test_invalid_interest_rate(self):
        """Test invalid interest rate raises error"""
        assets = [
            AssetInput(
                id="id-1",
                nominal_value=100,
                due_date="2025-12-04",
                interest_rate=1.5,
            )
        ]
        with pytest.raises(ValueError, match="invalid interest_rate"):
            validate_assets_input(assets)

    def test_duplicate_ids(self):
        """Test duplicate IDs raise error"""
        assets = [
            AssetInput(
                id="id-1",
                nominal_value=100,
                due_date="2025-12-04",
                interest_rate=0.05,
            ),
            AssetInput(
                id="id-1",
                nominal_value=50,
                due_date="2025-12-04",
                interest_rate=0.03,
            ),
        ]
        with pytest.raises(ValueError, match="Duplicate asset id"):
            validate_assets_input(assets)

    def test_empty_list(self):
        """Test empty list raises error"""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_assets_input([])


class TestPrepareAssetOutput:
    """Test asset output preparation"""

    def test_prepare_with_status(self):
        """Test preparing asset output with status"""
        future_date = (datetime.now(UTC) + timedelta(days=365)).strftime("%Y-%m-%d")
        asset_data = AssetData(
            id="id-1",
            nominal_value=100,
            due_date=future_date,
            interest_rate=0.05,
        )
        output = prepare_asset_output(asset_data)
        assert output.id == "id-1"
        assert output.status == "active"
        assert output.nominal_value == 100


class TestInsightsCalculation:
    """Test insights calculation"""

    def test_empty_portfolio(self):
        """Test insights with no assets"""
        clear_assets()
        insights = calculate_insights()
        assert insights == []

    def test_single_asset_insights(self):
        """Test insights with single asset"""
        clear_assets()
        store_asset(
            "id-1",
            AssetData(
                id="id-1",
                nominal_value=100,
                due_date="2025-12-04",
                interest_rate=0.05,
            ),
        )
        insights = calculate_insights()
        assert len(insights) == 2

        insights_dict = {i.name: i.value for i in insights}
        assert insights_dict["total_nominal_value"] == 100
        assert insights_dict["average_interest_rate"] == 0.05

    def test_multiple_assets_insights(self):
        """Test insights with multiple assets"""
        clear_assets()
        store_asset(
            "id-1",
            AssetData(
                id="id-1",
                nominal_value=100,
                due_date="2025-12-04",
                interest_rate=0.03,
            ),
        )
        store_asset(
            "id-2",
            AssetData(
                id="id-2",
                nominal_value=10,
                due_date="2026-01-04",
                interest_rate=0.1,
            ),
        )
        store_asset(
            "id-3",
            AssetData(
                id="id-3",
                nominal_value=30,
                due_date="2025-11-04",
                interest_rate=0.05,
            ),
        )

        insights = calculate_insights()
        assert len(insights) == 2

        insights_dict = {i.name: i.value for i in insights}
        assert insights_dict["total_nominal_value"] == 140
        # Average: (0.03 + 0.1 + 0.05) / 3 = 0.06
        assert abs(insights_dict["average_interest_rate"] - 0.06) < 1e-9
