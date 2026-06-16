from pathlib import Path
import os

APP_NAME = "NeuraFind"

APP_DATA_DIR = (
    Path(os.getenv("LOCALAPPDATA", Path.home()))
    / APP_NAME
)

DATA_DIR = APP_DATA_DIR / "data"
MODELS_DIR = APP_DATA_DIR / "models"
CACHE_DIR = APP_DATA_DIR / "cache"
LOGS_DIR = APP_DATA_DIR / "logs"
CONFIG_DIR = APP_DATA_DIR / "config"

for directory in (
    APP_DATA_DIR,
    DATA_DIR,
    MODELS_DIR,
    CACHE_DIR,
    LOGS_DIR,
    CONFIG_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "neurafind.db"
