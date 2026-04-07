"""Build a normalized JSONL file from Swedish general practice cases."""

from __future__ import annotations

import json
import re
from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import CLINICAL_CASE_MCQ


SOURCE_PATH = (
    Path(__file__).resolve().parents[3]
    / "swedish-medical-benchmark"
    / "benchmarks/specialist_questions/gp/fall_description_clinical_format.json"
)


def _parse_case_question(text: str) -> tuple[str, tuple[str, ...]]:
    if "Options:" not in text:
        return text.strip(), tuple()
    body, options_block = text.rsplit("Options:", 1)
    options = tuple(
        match.strip()
        for match in re.findall(r"[A-D]\)\s.*?(?=,\s*[A-D]\)\s|$)", options_block)
    )
    return body.strip(), options


def _normalize_option(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _match_label(answer: str, options: tuple[str, ...]) -> str:
    normalized_answer = _normalize_option(answer)
    for option in options:
        if _normalize_option(option) == normalized_answer:
            return option
    raise ValueError(f"Could not match answer {answer!r} to parsed options.")


def main() -> None:
    """Write the migrated Swedish general practice dataset to JSONL."""
    raw_data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    records: list[DatasetRecord] = []

    for raw_id, row in raw_data.items():
        question, options = _parse_case_question(row["Question"])
        if len(options) < 2:
            continue
        label = _match_label(row["Answer"], options)
        records.append(
            DatasetRecord(
                id=f"se-gp-sv-{raw_id}",
                language="sv",
                country="SE",
                dataset_name="se-gp-sv",
                task=CLINICAL_CASE_MCQ.name,
                source_type="general practice case questions",
                source_url="https://github.com/BirgerMoell/swedish-medical-benchmark",
                license="TBD per source",
                split="train",
                question=question,
                options=options,
                label=label,
                native_or_translated="native",
            )
        )

    output_path = Path("data/processed/se_gp_sv.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
