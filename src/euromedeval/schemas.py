"""Data models used by EuroMedEval."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path


class _StringEnum(str, Enum):
    """Backport-friendly string enum."""

    def __str__(self) -> str:
        return str(self.value)


class DatasetTier(_StringEnum):
    """Dataset maturity and intent tier."""

    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


class DatasetStatus(_StringEnum):
    """Leaderboard status."""

    OFFICIAL = "official"
    UNOFFICIAL = "unofficial"


class AccessMode(_StringEnum):
    """How users can access the dataset."""

    OPEN = "open"
    SCRIPT_ONLY = "script-only"
    PERMISSIONED = "permissioned"


class RecordFormat(_StringEnum):
    """How a record should be interpreted and scored."""

    MCQ = "mcq"
    EXTRACTIVE_QA = "extractive-qa"
    GENERATIVE_QA = "generative-qa"


@dataclass(frozen=True)
class DatasetRecord:
    """A normalized medical benchmark example."""

    id: str
    language: str
    country: str
    dataset_name: str
    task: str
    source_type: str
    source_url: str
    license: str
    split: str
    question: str
    record_format: RecordFormat = RecordFormat.MCQ
    options: tuple[str, ...] = field(default_factory=tuple)
    label: str | None = None
    context: str | None = None
    answers: tuple[str, ...] = field(default_factory=tuple)
    year: int | None = None
    specialty: str | None = None
    exam_name: str | None = None
    difficulty: str | None = None
    case_type: str | None = None
    evidence_source: str | None = None
    review_status: str | None = None
    reviewed_by: tuple[str, ...] = field(default_factory=tuple)
    native_or_translated: str = "native"
    translation_method: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if self.record_format == RecordFormat.MCQ:
            if len(self.options) < 2:
                raise ValueError("A multiple-choice record must have at least two options.")
            if self.label is None:
                raise ValueError("A multiple-choice record must have a label.")
            if self.label not in self.options:
                raise ValueError("The correct label must match one of the options exactly.")
            return

        if self.label is not None and self.label not in self.answers:
            raise ValueError("If set, label must match one of the reference answers.")
        if not self.answers:
            raise ValueError("QA-style records must include at least one reference answer.")

    def to_json(self) -> str:
        """Serialize the record as JSON."""
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass(frozen=True)
class DatasetConfig:
    """Metadata describing a benchmark dataset."""

    name: str
    pretty_name: str
    language: str
    country: str
    task: str
    tier: DatasetTier
    status: DatasetStatus
    source_url: str
    source_type: str
    license: str
    access_mode: AccessMode
    native: bool
    clinically_reviewed: bool
    creation_script: str
    description: str
    record_format: RecordFormat = RecordFormat.MCQ
    notes: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Return the config as a plain dictionary."""
        return asdict(self)


def write_records_to_jsonl(records: list[DatasetRecord], output_path: Path) -> None:
    """Write normalized records to a JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(record.to_json() + "\n")
