"""Build a normalized JSONL file from NorMedQA."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def _extract_options(row: dict) -> tuple[str, ...]:
    """Build option tuple from an answer + wrong answer payload."""
    correct = str(row.get("answer", "")).strip()
    raw_wrong = row.get("wrong_answers")
    if isinstance(raw_wrong, str):
        wrong = [item.strip() for item in raw_wrong.split(";") if item.strip()]
    elif isinstance(raw_wrong, list):
        wrong = [str(item).strip() for item in raw_wrong if str(item).strip()]
    else:
        wrong = []

    if not correct:
        return tuple(wrong)

    ordered = [correct, *wrong]
    # Keep order but de-duplicate deterministically.
    unique = []
    seen = set()
    for item in ordered:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return tuple(unique)


def main() -> None:
    """Write a small reproducible sample from NorMedQA records."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        output_path = Path("data/processed/nor_medqa_demo.jsonl")
        records.append(
            DatasetRecord(
                id="nor_medqa-demo-1",
                language="no",
                country="NO",
                dataset_name="normedqa-no",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="medical question answering from Norwegian exam sources",
                source_url="https://huggingface.co/datasets/SimulaMet/NorMedQA",
                license="CC BY 4.0",
                split="demo",
                question="Hvilken av følgende diagnoser er mest forenlig med plutselig åndenød, brysttetthet og hoste?",
                options=("Lungeemboli", "Ryggsmerte", "Pneumoni", "Nefritt"),
                label="Lungeemboli",
            )
        )
        write_records_to_jsonl(records, output_path)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{output_path}"
        )
        return

    dataset = load_dataset("SimulaMet/NorMedQA", split="train")
    limit = min(5000, len(dataset))

    for idx in range(limit):
        row = dataset[idx]
        question = str(row.get("question", "")).strip()
        options = _extract_options(row)
        label = str(row.get("answer", "")).strip()

        if not question or len(options) < 2:
            continue
        if label not in options:
            continue

        records.append(
            DatasetRecord(
                id=f"normedqa-no-{idx}",
                language="no",
                country="NO",
                dataset_name="normedqa-no",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="medical question answering from Norwegian exam sources",
                source_url="https://huggingface.co/datasets/SimulaMet/NorMedQA",
                license="CC BY 4.0",
                split="train",
                question=question,
                options=options,
                label=label,
                year=2024,
                exam_name=row.get("exam_name", "") if isinstance(row.get("exam_name"), str) else None,
                specialty=row.get("specialty", "") if isinstance(row.get("specialty"), str) else None,
            )
        )

    output_path = Path("data/processed/nor_medqa.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()

