"""Minimal scoring utilities for EuroMedEval."""

from __future__ import annotations

import math
import random
import statistics
import re
import string
from dataclasses import dataclass, field
from typing import Iterable

from .schemas import DatasetRecord, RecordFormat


@dataclass(frozen=True)
class DatasetScore:
    """Score summary for one dataset."""

    dataset_name: str
    language: str
    task: str
    native: bool
    primary_metric: str
    primary_score: float
    ci_low: float
    ci_high: float
    sample_size: int
    secondary_metrics: dict[str, float] = field(default_factory=dict)


class Benchmarker:
    """A minimal benchmarker for normalized medical datasets."""

    def __init__(self, *, bootstrap_iterations: int = 200, seed: int = 13) -> None:
        self.bootstrap_iterations = bootstrap_iterations
        self.seed = seed

    def score_mcq(
        self,
        *,
        dataset_name: str,
        language: str,
        task: str,
        native: bool,
        records: Iterable[DatasetRecord],
        predictions: dict[str, str],
    ) -> DatasetScore:
        """Score a set of MCQ predictions against normalized records."""
        examples = list(records)
        if not examples:
            raise ValueError("Cannot score an empty dataset.")

        gold = [example.label for example in examples]
        pred = [predictions[example.id] for example in examples]
        accuracy = _accuracy(gold=gold, pred=pred)
        ci_low, ci_high = _bootstrap_accuracy_interval(
            gold=gold,
            pred=pred,
            iterations=self.bootstrap_iterations,
            seed=self.seed,
        )
        return DatasetScore(
            dataset_name=dataset_name,
            language=language,
            task=task,
            native=native,
            primary_metric="accuracy",
            primary_score=accuracy,
            ci_low=ci_low,
            ci_high=ci_high,
            sample_size=len(examples),
        )

    def score_qa(
        self,
        *,
        dataset_name: str,
        language: str,
        task: str,
        native: bool,
        records: Iterable[DatasetRecord],
        predictions: dict[str, str],
    ) -> DatasetScore:
        """Score QA predictions with exact match as the primary metric."""
        examples = list(records)
        if not examples:
            raise ValueError("Cannot score an empty dataset.")

        exact_match_values: list[float] = []
        f1_values: list[float] = []
        for example in examples:
            prediction = predictions[example.id]
            references = example.answers or ((example.label,) if example.label else tuple())
            exact_match_values.append(_best_exact_match(prediction=prediction, references=references))
            f1_values.append(_best_f1(prediction=prediction, references=references))

        ci_low, ci_high = _bootstrap_binary_interval(
            values=exact_match_values,
            iterations=self.bootstrap_iterations,
            seed=self.seed,
        )
        return DatasetScore(
            dataset_name=dataset_name,
            language=language,
            task=task,
            native=native,
            primary_metric="exact_match",
            primary_score=statistics.fmean(exact_match_values),
            ci_low=ci_low,
            ci_high=ci_high,
            sample_size=len(examples),
            secondary_metrics={"token_f1": statistics.fmean(f1_values)},
        )

    def score_records(
        self,
        *,
        dataset_name: str,
        language: str,
        task: str,
        native: bool,
        records: Iterable[DatasetRecord],
        predictions: dict[str, str],
    ) -> DatasetScore:
        """Dispatch scoring based on record format."""
        examples = list(records)
        if not examples:
            raise ValueError("Cannot score an empty dataset.")

        if examples[0].record_format == RecordFormat.MCQ:
            return self.score_mcq(
                dataset_name=dataset_name,
                language=language,
                task=task,
                native=native,
                records=examples,
                predictions=predictions,
            )

        return self.score_qa(
            dataset_name=dataset_name,
            language=language,
            task=task,
            native=native,
            records=examples,
            predictions=predictions,
        )


def aggregate_language_scores(scores: Iterable[DatasetScore]) -> dict[str, float]:
    """Aggregate native dataset scores by task family, then by language.

    The flagship aggregation is native-only, equal-weight-by-task.
    """
    native_scores = [score for score in scores if score.native]
    if not native_scores:
        return {}

    task_to_values: dict[str, list[float]] = {}
    for score in native_scores:
        task_to_values.setdefault(score.task, []).append(score.primary_score)

    task_means = [statistics.fmean(values) for values in task_to_values.values()]
    return {
        "native_task_weighted_accuracy": statistics.fmean(task_means),
        "num_native_datasets": float(len(native_scores)),
        "num_task_families": float(len(task_means)),
    }


def _accuracy(*, gold: list[str], pred: list[str]) -> float:
    if len(gold) != len(pred):
        raise ValueError("Gold labels and predictions must have the same length.")
    correct = sum(1 for gold_label, pred_label in zip(gold, pred) if gold_label == pred_label)
    return correct / len(gold)


def _bootstrap_accuracy_interval(
    *,
    gold: list[str],
    pred: list[str],
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(gold)
    if n == 1:
        value = _accuracy(gold=gold, pred=pred)
        return value, value

    samples: list[float] = []
    indices = list(range(n))
    for _ in range(iterations):
        sample_idx = [rng.choice(indices) for _ in range(n)]
        sample_gold = [gold[idx] for idx in sample_idx]
        sample_pred = [pred[idx] for idx in sample_idx]
        samples.append(_accuracy(gold=sample_gold, pred=sample_pred))

    mean = statistics.fmean(samples)
    if len(samples) == 1:
        return mean, mean
    std = statistics.stdev(samples)
    sem = std / math.sqrt(len(samples))
    margin = 1.96 * sem
    return max(0.0, mean - margin), min(1.0, mean + margin)


def _bootstrap_binary_interval(
    *,
    values: list[float],
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    if n == 1:
        return values[0], values[0]

    samples: list[float] = []
    indices = list(range(n))
    for _ in range(iterations):
        sample_idx = [rng.choice(indices) for _ in range(n)]
        samples.append(statistics.fmean(values[idx] for idx in sample_idx))

    mean = statistics.fmean(samples)
    if len(samples) == 1:
        return mean, mean
    std = statistics.stdev(samples)
    sem = std / math.sqrt(len(samples))
    margin = 1.96 * sem
    return max(0.0, mean - margin), min(1.0, mean + margin)


def _best_exact_match(*, prediction: str, references: tuple[str, ...]) -> float:
    normalized_prediction = _normalize_text(prediction)
    for reference in references:
        if normalized_prediction == _normalize_text(reference):
            return 1.0
    return 0.0


def _best_f1(*, prediction: str, references: tuple[str, ...]) -> float:
    scores = [_token_f1(prediction=prediction, reference=reference) for reference in references]
    return max(scores) if scores else 0.0


def _token_f1(*, prediction: str, reference: str) -> float:
    pred_tokens = _normalize_text(prediction).split()
    ref_tokens = _normalize_text(reference).split()
    if not pred_tokens and not ref_tokens:
        return 1.0
    if not pred_tokens or not ref_tokens:
        return 0.0

    overlap: dict[str, int] = {}
    for token in pred_tokens:
        overlap[token] = overlap.get(token, 0) + 1

    common = 0
    for token in ref_tokens:
        count = overlap.get(token, 0)
        if count > 0:
            common += 1
            overlap[token] = count - 1

    if common == 0:
        return 0.0

    precision = common / len(pred_tokens)
    recall = common / len(ref_tokens)
    return (2 * precision * recall) / (precision + recall)


def _normalize_text(text: str) -> str:
    lowered = text.lower().strip()
    table = str.maketrans("", "", string.punctuation)
    no_punctuation = lowered.translate(table)
    return re.sub(r"\s+", " ", no_punctuation)
