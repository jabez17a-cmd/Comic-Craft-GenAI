from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = Field("ComicCraft", validation_alias="APP_NAME")
    debug: bool = Field(True, validation_alias="DEBUG")

    gemini_api_key: str = Field("", validation_alias="GEMINI_API_KEY")
    hf_token: str = Field("", validation_alias="HF_TOKEN")

    gemini_outline_model: str = Field(
        "gemini-3.8-flash",
        validation_alias="GEMINI_OUTLINE_MODEL",
    )

    gemini_story_model: str = Field(
        "gemini-3.5-flash-lite",
        validation_alias="GEMINI_STORY_MODEL",
    )

    image_model: str = Field(
        "black-forest-labs/FLUX.1-schnell",
        validation_alias="IMAGE_MODEL",
    )

    panel_count: int = Field(
        5,
        validation_alias="PANEL_COUNT",
        ge=1,
        le=10,
    )

    image_width: int = Field(
        768,
        validation_alias="IMAGE_WIDTH",
        ge=256,
        le=1536,
    )

    image_height: int = Field(
        768,
        validation_alias="IMAGE_HEIGHT",
        ge=256,
        le=1536,
    )

    image_steps: int = Field(
        4,
        validation_alias="IMAGE_STEPS",
        ge=1,
        le=100,
    )

    image_guidance_scale: float = Field(
        3.5,
        validation_alias="IMAGE_GUIDANCE_SCALE",
        ge=1,
        le=30,
    )

    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"
    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "exports"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    def ensure_directories(self) -> None:
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings