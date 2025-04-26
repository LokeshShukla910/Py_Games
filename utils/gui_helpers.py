import os

def get_asset_path(filename):
    """
    Returns the absolute path to the asset file.
    Assumes assets are stored in an 'assets' folder in the project directory.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Go up one level to the project root
    assets_dir = os.path.join(base_dir, "assets")
    if not os.path.exists(assets_dir):
        raise FileNotFoundError(f"Assets directory not found: {assets_dir}")
    asset_path = os.path.join(assets_dir, filename)
    if not os.path.exists(asset_path):
        raise FileNotFoundError(f"Asset file not found: {asset_path}")
    return asset_path