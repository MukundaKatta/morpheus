"""Configuration for Morpheus."""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class MorpheusConfig(BaseSettings):
    model_config = {"env_prefix": "MORPHEUS_", "env_file": ".env"}

    api_key: str = Field(default="", alias="OPENAI_API_KEY")
    default_model: str = Field(default="gpt-4", alias="DEFAULT_MODEL")
    workspace_dir: Path = Field(default=Path("./workspace"), alias="WORKSPACE_DIR")
    max_iterations: int = Field(default=3, alias="MAX_ITERATIONS")


def load_config() -> MorpheusConfig:
    return MorpheusConfig()
