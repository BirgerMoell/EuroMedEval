"""Dataset registry."""

from __future__ import annotations

from .dataset_configs import ALL_DATASET_CONFIGS
from .schemas import DatasetConfig


def list_dataset_configs(language: str | None = None) -> list[DatasetConfig]:
    """List dataset configs, optionally filtered by language."""
    configs = list(ALL_DATASET_CONFIGS)
    if language is None:
        return configs
    return [config for config in configs if config.language == language]


def get_dataset_config(name: str) -> DatasetConfig:
    """Get a dataset config by name."""
    for config in ALL_DATASET_CONFIGS:
        if config.name == name:
            return config
    raise KeyError(f"Unknown dataset config: {name}")

