"""Build a normalized JSONL file from the Swedish doctors exam benchmark."""

from __future__ import annotations

import json
import re
from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


SOURCE_PATH = (
    Path(__file__).resolve().parents[3]
    / "swedish-medical-benchmark"
    / "benchmarks/swetheoreticaldoctorsexam/clinical_case.json"
)


def _parse_question_block(text: str) -> tuple[str, tuple[str, ...]]:
    marker = "*Välj ett alternativ:*"
    if marker not in text:
        return text.strip(), tuple()
    stem, options_block = text.split(marker, 1)
    options = tuple(match.strip() for match in re.findall(r"(?m)^[a-e]\)\s.*$", options_block))
    return stem.strip(), options


def _normalize_option(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _match_label(answer: str, options: tuple[str, ...]) -> str:
    normalized_answer = _normalize_option(answer)
    for option in options:
        if _normalize_option(option) == normalized_answer:
            return option
    raise ValueError(f"Could not match answer {answer!r} to parsed options.")


def main() -> None:
    """Write the migrated Swedish doctors exam to processed JSONL."""
    raw_data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    records: list[DatasetRecord] = []

    for raw_id, row in raw_data.items():
        question, options = _parse_question_block(row["QUESTION"])
        if len(options) < 2:
            continue
        label = _match_label(row["ANSWER"], options)
        records.append(
            DatasetRecord(
                id=f"smdt-sv-{raw_id}",
                language="sv",
                country="SE",
                dataset_name="smdt-sv",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="medical licensing-style exam",
                source_url="https://github.com/BirgerMoell/swedish-medical-benchmark",
                license="TBD per source",
                split="train",
                question=question,
                options=options,
                label=label,
                exam_name=row.get("EXAM"),
                native_or_translated="native",
            )
        )

    output_path = Path("data/processed/smdt_sv.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
