"""In-memory storage for assets"""

from backend.src.models import AssetData

# Global in-memory storage for assets
assets_store: dict[str, AssetData] = {}


def store_asset(asset_id: str, asset_data: AssetData) -> None:
    """Store or update an asset"""
    assets_store[asset_id] = asset_data


def get_all_assets() -> list[AssetData]:
    """Get all stored assets"""
    return list(assets_store.values())


def get_asset(asset_id: str) -> AssetData | None:
    """Get a specific asset by ID"""
    return assets_store.get(asset_id)


def clear_assets() -> None:
    """Clear all assets (useful for testing)"""
    assets_store.clear()


def asset_count() -> int:
    """Get the number of stored assets"""
    return len(assets_store)
