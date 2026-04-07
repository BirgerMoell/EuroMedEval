"""EuroMedEval package."""

from .benchmarker import Benchmarker, DatasetScore, aggregate_language_scores
from .builders import build_all, build_dataset
from .registry import get_dataset_config, list_dataset_configs

__all__ = [
    "Benchmarker",
    "DatasetScore",
    "aggregate_language_scores",
    "build_all",
    "build_dataset",
    "get_dataset_config",
    "list_dataset_configs",
]
