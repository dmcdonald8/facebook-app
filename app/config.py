from pydantic import BaseSettings
from pathlib import Path
import toml

ROOT_DIR = Path(__file__).parents[1]

VERSION = (
    toml.load(f"{ROOT_DIR}/pyproject.toml")
    .get("tool", {})
    .get("poetry", {})
    .get("version", "")
)


class Settings(BaseSettings):
    api_version: str = "v1"
    url_prefix: str = "api"
    max_facebook_pages: int = 10
