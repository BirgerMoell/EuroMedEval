"""Helpers for running dataset build scripts."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

from .registry import get_dataset_config, list_dataset_configs


def project_root() -> Path:
    """Return the repository root for the editable source tree."""
    return Path(__file__).resolve().parents[2]


def build_dataset(name: str) -> Path:
    """Run the creation script for one registered dataset."""
    config = get_dataset_config(name)
    root = project_root()
    script_path = root / config.creation_script
    if not script_path.exists():
        raise FileNotFoundError(f"Creation script not found: {script_path}")

    original_cwd = Path.cwd()
    original_sys_path = list(sys.path)
    os.environ["EUROMEDEVAL_DATASET_NAME"] = name
    try:
        os.chdir(root)
        src_path = str(root / "src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        runpy.run_path(str(script_path), run_name="__main__")
    finally:
        os.chdir(original_cwd)
        sys.path[:] = original_sys_path
        os.environ.pop("EUROMEDEVAL_DATASET_NAME", None)

    return script_path


def build_all(language: str | None = None) -> list[str]:
    """Run creation scripts for all registered datasets."""
    built: list[str] = []
    for config in list_dataset_configs(language=language):
        build_dataset(config.name)
        built.append(config.name)
    return built
