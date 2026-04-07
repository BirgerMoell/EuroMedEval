"""Build a normalized JSONL file from the Polish PES specialist exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_answer_letter, parse_inline_lettered_mcq
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


DATASET_ID = "amu-cai/medical-exams-PES-PL-2007-2024"
DATASET_NAME = "pes-pl"
OUTPUT_PATH = Path("data/processed/pes_pl.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/pes_pl_demo.jsonl")
PRETTY_SOURCE = "specialist board certification exam"


def main() -> None:
    """Extract PES questions into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="pes-pl-demo-1",
                language="pl",
                country="PL",
                dataset_name=DATASET_NAME,
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type=PRETTY_SOURCE,
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="See upstream source and CEM terms",
                split="demo",
                question="Wskaż zdanie fałszywe dotyczące sedacji i znieczulenia ogólnego do leczenia stomatologicznego.",
                options=(
                    "A. Sedacja wziewna do 50% podtlenku azotu może być wykonana przez stomatologa z pomocą asystenta",
                    "B. Osoby ASA I i ASA II można bezpiecznie poddać płytkiej sedacji ambulatoryjnej",
                    "C. Stosowanie sedacji dożylnej wymaga obecności anestezjologa",
                    "D. Sedacja z użyciem N2O nie wymaga dodatkowego działania przeciwbólowego",
                    "E. Najdogodniejsza jest intubacja drogą nosowo-tchawiczą",
                ),
                label="D. Sedacja z użyciem N2O nie wymaga dodatkowego działania przeciwbólowego",
                exam_name="PES 2018 wiosna",
                specialty="stomatologia dziecięca",
                native_or_translated="native",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{DEMO_OUTPUT_PATH}"
        )
        return

    dataset = load_dataset(DATASET_ID, split="train")

    for row in dataset:
        question, options = parse_inline_lettered_mcq(str(row.get("question", "")))
        label = label_from_answer_letter(str(row.get("answer", "")), options)
        if not question or len(options) < 2 or label is None:
            continue

        year = row.get("year")
        specialty = str(row.get("specialty", "")).strip() or None
        edition = str(row.get("edition", "")).strip() or "PES"

        records.append(
            DatasetRecord(
                id=f"pes-pl-{edition}-{row.get('question_id', len(records))}",
                language="pl",
                country="PL",
                dataset_name=DATASET_NAME,
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type=PRETTY_SOURCE,
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="See upstream source and CEM terms",
                split="train",
                question=question,
                options=options,
                label=label,
                year=int(year) if year is not None else None,
                specialty=specialty,
                exam_name=edition,
                native_or_translated="native",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
