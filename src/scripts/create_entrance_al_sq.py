"""Build a normalized JSONL file from the Albanian medical entrance exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_one_based_index
from euromedeval.tasks import MEDICAL_ENTRANCE_MCQ


DATASET_ID = "marjpri/albanian-medical-exams-cycles-mcq-190"
DATASET_NAME = "entrance-al-sq"
OUTPUT_PATH = Path("data/processed/entrance_al_sq.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/entrance_al_sq_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    raw = row.get("options")
    if not isinstance(raw, list):
        return tuple()
    return tuple(str(option).strip() for option in raw if str(option).strip())


def main() -> None:
    """Extract Albanian medical entrance questions into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="entrance-al-sq-demo-1",
                language="sq",
                country="AL",
                dataset_name=DATASET_NAME,
                task=MEDICAL_ENTRANCE_MCQ.name,
                source_type="digital medical entrance examination",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="Derived from public official exam material on QSHA",
                split="demo",
                question="Gjatë procesit të fotosintezës energjia e fotoneve të dritës depozitohet fillimisht në molekula si:",
                options=("aminoacide", "NADPH + ATP", "RDP-së", "glukozës"),
                label="NADPH + ATP",
                specialty="medicine",
                exam_name="QSHA digital medicine exam",
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
        question = str(row.get("question", "")).strip()
        options = _safe_options(row)
        label = label_from_one_based_index(str(row.get("answer", "")), options)
        if not question or len(options) < 2 or label is None:
            continue

        records.append(
            DatasetRecord(
                id=f"entrance-al-sq-{row.get('original_question_num', len(records))}",
                language="sq",
                country="AL",
                dataset_name=DATASET_NAME,
                task=MEDICAL_ENTRANCE_MCQ.name,
                source_type="digital medical entrance examination",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="Derived from public official exam material on QSHA",
                split="train",
                question=question,
                options=options,
                label=label,
                specialty=str(row.get("category_en", "")).strip() or None,
                exam_name="QSHA digital medicine exam",
                native_or_translated="native",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
