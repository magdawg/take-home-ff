"""Tests for Pydantic models"""

import json

import pytest

from backend.src.models import AssetInput, AssetOutput, Insight


class TestAssetInputModel:
    """Test AssetInput validation"""

    def test_valid_asset_input(self):
        """Test creating valid asset input"""
        asset = AssetInput(
            id="id-1",
            nominal_value=100,
            due_date="2025-12-04",
            interest_rate=0.05,
        )
        assert asset.id == "id-1"
        assert asset.nominal_value == 100
        assert asset.interest_rate == 0.05

    def test_asset_input_from_json(self):
        """Test creating asset from dict"""
        data = {
            "id": "id-2",
            "nominal_value": 50.5,
            "due_date": "2025-12-04",
            "interest_rate": 0.03,
        }
        asset = AssetInput(**data)
        assert asset.nominal_value == 50.5

    def test_asset_input_schema(self):
        """Test schema includes example"""
        schema = AssetInput.model_json_schema()
        # Pydantic v2 puts example at top level, not in $defs
        assert "example" in schema


class TestAssetOutputModel:
    """Test AssetOutput validation"""

    def test_valid_asset_output(self):
        """Test creating valid asset output"""
        asset = AssetOutput(
            id="id-1",
            nominal_value=100,
            status="active",
            due_date="2025-12-04",
        )
        assert asset.status in ["active", "defaulted"]

    def test_asset_output_serialization(self):
        """Test serializing asset output"""
        asset = AssetOutput(
            id="id-1",
            nominal_value=100.5,
            status="defaulted",
            due_date="2025-12-04",
        )
        data = asset.model_dump()
        assert data["nominal_value"] == 100.5
        assert data["status"] == "defaulted"


class TestInsightModel:
    """Test Insight validation"""

    def test_valid_insight(self):
        """Test creating valid insight"""
        insight = Insight(
            id="insight-1",
            name="total_nominal_value",
            value=140.0,
        )
        assert insight.name == "total_nominal_value"
        assert insight.value == 140.0

    def test_insight_serialization(self):
        """Test serializing insight"""
        insight = Insight(
            id="insight-2",
            name="average_interest_rate",
            value=0.06,
        )
        data = insight.model_dump()
        assert data["value"] == 0.06
