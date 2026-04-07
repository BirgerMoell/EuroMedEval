"""Build a normalized JSONL file from manually prepared IMPP sample-question exports."""

from __future__ import annotations

import json
from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_answer_letter
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


DATASET_NAME = "impp-sample-de"
RAW_PATH = Path("data/raw/impp/impp_sample_de.json")
OUTPUT_PATH = Path("data/processed/impp_sample_de.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/impp_sample_de_demo.jsonl")
SOURCE_URL = "https://www.impp.de/pruefungen/medizin/beispielaufgaben.html"


def _safe_options(row: dict) -> tuple[str, ...]:
    raw = row.get("options")
    if isinstance(raw, list):
        options = []
        for idx, value in enumerate(raw):
            text = str(value).strip()
            if not text:
                continue
            letter = chr(ord("A") + idx)
            options.append(f"{letter}. {text}")
        return tuple(options)
    return tuple()


def main() -> None:
    """Convert a manually prepared IMPP sample export into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    if not RAW_PATH.exists():
        records.append(
            DatasetRecord(
                id="impp-sample-de-demo-1",
                language="de",
                country="DE",
                dataset_name=DATASET_NAME,
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="official state exam sample questions",
                source_url=SOURCE_URL,
                license="Copyrighted official sample tasks; use subject to IMPP terms",
                split="demo",
                question="Welche Aussage zur Hyperthyreose trifft am ehesten zu?",
                options=(
                    "A. Sie führt regelhaft zu Bradykardie.",
                    "B. Sie kann mit Gewichtsverlust und Tachykardie einhergehen.",
                    "C. Sie ist immer autoimmun bedingt.",
                    "D. Sie verursacht typischerweise Hypothermie.",
                    "E. Sie ist mit supprimiertem TSH unvereinbar.",
                ),
                label="B. Sie kann mit Gewichtsverlust und Tachykardie einhergehen.",
                exam_name="IMPP Beispielaufgaben M2",
                year=2024,
                specialty="Innere Medizin",
                native_or_translated="native",
                notes=(
                    "Full conversion requires a manual local export because the official IMPP "
                    "source restricts automated reuse."
                ),
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "Manual source file not found. Place a local export at "
            f"{RAW_PATH} to build the full dataset. Wrote demo record to {DEMO_OUTPUT_PATH}"
        )
        return

    raw_rows = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    for index, row in enumerate(raw_rows):
        question = str(row.get("question", "")).strip()
        options = _safe_options(row)
        label = label_from_answer_letter(str(row.get("answer_letter", "")), options)
        if not question or len(options) < 2 or label is None:
            continue

        year = row.get("year")
        records.append(
            DatasetRecord(
                id=str(row.get("id", f"impp-sample-de-{index}")),
                language="de",
                country="DE",
                dataset_name=DATASET_NAME,
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="official state exam sample questions",
                source_url=SOURCE_URL,
                license="Copyrighted official sample tasks; use subject to IMPP terms",
                split="manual",
                question=question,
                options=options,
                label=label,
                year=int(year) if year is not None else None,
                specialty=str(row.get("specialty", "")).strip() or None,
                exam_name=str(row.get("exam_name", "")).strip() or "IMPP Beispielaufgaben",
                native_or_translated="native",
                notes="Built from a manually prepared local export of the official sample questions.",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
