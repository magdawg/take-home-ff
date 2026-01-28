"""FastAPI routes and endpoint handlers"""

import logging

from fastapi import APIRouter, HTTPException

from backend.src.models import AssetData, AssetInput, AssetOutput, Insight
from backend.src.service import (
    calculate_insights,
    prepare_asset_output,
    validate_assets_input,
)
from backend.src.storage import get_all_assets, store_asset

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/asset")
async def create_assets(assets: list[AssetInput]):
    """
    Create or update assets.
    Accepts a list of assets and stores them in memory.
    """
    try:
        validate_assets_input(assets)

        for asset in assets:
            asset_data = AssetData(
                id=asset.id,
                nominal_value=asset.nominal_value,
                due_date=asset.due_date,
                interest_rate=asset.interest_rate,
            )
            store_asset(asset.id, asset_data)
            logger.info(f"Asset {asset.id} created/updated")

        return {"message": f"Successfully created/updated {len(assets)} assets"}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/asset")
async def get_assets() -> list[AssetOutput]:
    """
    Retrieve all assets with their current status.
    Status is determined based on due date compared to today (UTC).
    """
    try:
        result = []
        for asset_data in get_all_assets():
            result.append(prepare_asset_output(asset_data))
        logger.info(f"Retrieved {len(result)} assets")
        return result
    except Exception as e:
        logger.error(f"Error retrieving assets: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/insights")
async def get_insights() -> list[Insight]:
    """
    Generate insights from the current asset portfolio.
    Calculates metrics like average interest rate and total nominal value.
    """
    try:
        return calculate_insights()
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
