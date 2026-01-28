"""Business logic for asset management and insights calculation"""

import logging
from datetime import UTC, datetime

from backend.src.models import AssetData, AssetInput, AssetOutput, AssetStatus, Insight
from backend.src.storage import get_all_assets

logger = logging.getLogger(__name__)


def determine_asset_status(due_date_str: str) -> AssetStatus:
    """
    Determine asset status based on due date.
    Uses UTC today. Assets with due_date in the past are "defaulted", otherwise "active".
    """
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        today = datetime.now(UTC).date()
        return AssetStatus.DEFAULTED if due_date < today else AssetStatus.ACTIVE
    except ValueError as e:
        logger.error(f"Invalid date format: {due_date_str}. Error: {e}")
        raise ValueError(f"Invalid date format: {due_date_str}. Use YYYY-MM-DD.")


def validate_assets_input(assets: list[AssetInput]) -> None:
    """Validate input assets"""
    if not assets:
        raise ValueError("Assets list cannot be empty")
    if len(assets) > 10000:
        raise ValueError("Assets list too large (max 10000)")

    seen_ids = set()
    for asset in assets:
        if asset.nominal_value < 0:
            raise ValueError(f"Asset {asset.id} has negative nominal_value")
        if asset.interest_rate < 0 or asset.interest_rate > 1:
            raise ValueError(
                f"Asset {asset.id} has invalid interest_rate (must be 0-1)"
            )
        if asset.id in seen_ids:
            raise ValueError(f"Duplicate asset id: {asset.id}")
        seen_ids.add(asset.id)
        # Validate date format
        determine_asset_status(asset.due_date)


def prepare_asset_output(asset_data: AssetData) -> AssetOutput:
    """Convert stored asset data to output format with calculated status"""
    status = determine_asset_status(asset_data.due_date)
    return AssetOutput(
        id=asset_data.id,
        nominal_value=asset_data.nominal_value,
        status=status,
        due_date=asset_data.due_date,
    )


def calculate_insights() -> list[Insight]:
    """
    Generate insights from the current asset portfolio.
    Calculates metrics like average interest rate and total nominal value.
    """
    assets = get_all_assets()

    if not assets:
        logger.info("No assets in portfolio")
        return []

    # Calculate insights
    total_nominal_value = sum(asset.nominal_value for asset in assets)
    average_interest_rate = sum(asset.interest_rate for asset in assets) / len(assets)

    insights = [
        Insight(id="insight-1", name="total_nominal_value", value=total_nominal_value),
        Insight(
            id="insight-2",
            name="average_interest_rate",
            value=average_interest_rate,
        ),
    ]

    logger.info(f"Generated {len(insights)} insights")
    return insights
