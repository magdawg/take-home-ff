"""Tests for API routes and endpoints"""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.src.storage import clear_assets, store_asset

client = TestClient(app)


class TestCreateAssets:
    """Test POST /asset endpoint"""

    def test_create_single_asset(self):
        """Test creating a single asset"""
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 200
        assert "Successfully created" in response.json()["message"]

    def test_create_multiple_assets(self):
        """Test creating multiple assets"""
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            },
            {
                "id": "id-2",
                "nominal_value": 10,
                "due_date": "2026-01-04",
                "interest_rate": 0.1,
            },
            {
                "id": "id-3",
                "nominal_value": 30,
                "due_date": "2025-11-04",
                "interest_rate": 0.05,
            },
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 200

    def test_create_asset_with_negative_nominal_value(self):
        """Test creating asset with negative nominal value"""
        payload = [
            {
                "id": "id-neg",
                "nominal_value": -100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 400
        assert "negative nominal_value" in response.json()["detail"]

    def test_create_asset_with_invalid_interest_rate(self):
        """Test creating asset with invalid interest rate"""
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 1.5,
            }
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 400
        assert "invalid interest_rate" in response.json()["detail"]

    def test_create_asset_with_invalid_date_format(self):
        """Test creating asset with invalid date format"""
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025/12/04",
                "interest_rate": 0.03,
            }
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 400
        assert "Invalid date format" in response.json()["detail"]

    def test_create_asset_with_duplicate_ids(self):
        """Test creating assets with duplicate IDs"""
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            },
            {
                "id": "id-1",
                "nominal_value": 50,
                "due_date": "2025-12-04",
                "interest_rate": 0.05,
            },
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 400
        assert "Duplicate asset id" in response.json()["detail"]

    def test_create_empty_asset_list(self):
        """Test creating with empty list"""
        payload = []
        response = client.post("/asset", json=payload)
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]

    def test_update_existing_asset(self):
        """Test updating an existing asset"""
        payload1 = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        ]
        response1 = client.post("/asset", json=payload1)
        assert response1.status_code == 200

        payload2 = [
            {
                "id": "id-1",
                "nominal_value": 200,
                "due_date": "2025-12-05",
                "interest_rate": 0.05,
            }
        ]
        response2 = client.post("/asset", json=payload2)
        assert response2.status_code == 200


class TestGetAssets:
    """Test GET /asset endpoint"""

    def test_get_empty_assets(self):
        """Test retrieving assets when none exist"""
        clear_assets()
        response = client.get("/asset")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_single_asset_active(self):
        """Test retrieving a single active asset"""
        clear_assets()
        future_date = (datetime.now(UTC) + timedelta(days=365)).strftime("%Y-%m-%d")
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": future_date,
                "interest_rate": 0.03,
            }
        ]
        client.post("/asset", json=payload)

        response = client.get("/asset")
        assert response.status_code == 200
        assets = response.json()
        assert len(assets) == 1
        assert assets[0]["status"] == "active"

    def test_get_single_asset_defaulted(self):
        """Test retrieving a single defaulted asset"""
        clear_assets()
        past_date = (datetime.now(UTC) - timedelta(days=10)).strftime("%Y-%m-%d")
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": past_date,
                "interest_rate": 0.03,
            }
        ]
        client.post("/asset", json=payload)

        response = client.get("/asset")
        assert response.status_code == 200
        assets = response.json()
        assert len(assets) == 1
        assert assets[0]["status"] == "defaulted"

    def test_get_mixed_assets(self):
        """Test retrieving mix of active and defaulted assets"""
        clear_assets()
        future_date = (datetime.now(UTC) + timedelta(days=365)).strftime("%Y-%m-%d")
        past_date = (datetime.now(UTC) - timedelta(days=10)).strftime("%Y-%m-%d")

        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": future_date,
                "interest_rate": 0.03,
            },
            {
                "id": "id-2",
                "nominal_value": 50,
                "due_date": past_date,
                "interest_rate": 0.05,
            },
        ]
        client.post("/asset", json=payload)

        response = client.get("/asset")
        assert response.status_code == 200
        assets = response.json()
        assert len(assets) == 2

        statuses = {asset["id"]: asset["status"] for asset in assets}
        assert statuses["id-1"] == "active"
        assert statuses["id-2"] == "defaulted"

    def test_get_assets_returns_all_fields(self):
        """Test that returned assets have all required fields"""
        clear_assets()
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100.5,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        ]
        client.post("/asset", json=payload)

        response = client.get("/asset")
        assets = response.json()
        asset = assets[0]

        assert "id" in asset
        assert "nominal_value" in asset
        assert "status" in asset
        assert "due_date" in asset
        assert asset["nominal_value"] == 100.5


class TestGetInsights:
    """Test GET /insights endpoint"""

    def test_get_insights_empty(self):
        """Test getting insights with no assets"""
        clear_assets()
        response = client.get("/insights")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_insights_single_asset(self):
        """Test getting insights with single asset"""
        clear_assets()
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.05,
            }
        ]
        client.post("/asset", json=payload)

        response = client.get("/insights")
        assert response.status_code == 200
        insights = response.json()
        assert len(insights) == 2

        insights_dict = {insight["name"]: insight["value"] for insight in insights}
        assert insights_dict["total_nominal_value"] == 100
        assert insights_dict["average_interest_rate"] == 0.05

    def test_get_insights_multiple_assets(self):
        """Test getting insights with multiple assets"""
        clear_assets()
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            },
            {
                "id": "id-2",
                "nominal_value": 10,
                "due_date": "2026-01-04",
                "interest_rate": 0.1,
            },
            {
                "id": "id-3",
                "nominal_value": 30,
                "due_date": "2025-11-04",
                "interest_rate": 0.05,
            },
        ]
        client.post("/asset", json=payload)

        response = client.get("/insights")
        assert response.status_code == 200
        insights = response.json()
        assert len(insights) == 2

        insights_dict = {insight["name"]: insight["value"] for insight in insights}
        assert insights_dict["total_nominal_value"] == 140
        assert abs(insights_dict["average_interest_rate"] - 0.06) < 1e-9


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestIntegration:
    """Integration tests"""

    def test_full_workflow(self):
        """Test complete workflow: create, retrieve, get insights"""
        clear_assets()

        # Create assets
        payload = [
            {
                "id": "id-1",
                "nominal_value": 100,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            },
            {
                "id": "id-2",
                "nominal_value": 10,
                "due_date": "2026-01-04",
                "interest_rate": 0.1,
            },
            {
                "id": "id-3",
                "nominal_value": 30,
                "due_date": "2025-11-04",
                "interest_rate": 0.05,
            },
        ]
        response = client.post("/asset", json=payload)
        assert response.status_code == 200

        # Retrieve assets
        response = client.get("/asset")
        assert response.status_code == 200
        assets = response.json()
        assert len(assets) == 3

        # Get insights
        response = client.get("/insights")
        assert response.status_code == 200
        insights = response.json()
        assert len(insights) == 2

        insights_dict = {insight["name"]: insight["value"] for insight in insights}
        assert insights_dict["total_nominal_value"] == 140
