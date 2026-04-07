"""Build a normalized JSONL file from the Belgian physician entrance exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_one_based_index
from euromedeval.tasks import MEDICAL_ENTRANCE_MCQ


DATASET_ID = "jjzha/belgian-entrance-exam-physician"
DATASET_NAME = "entrance-be-nl"
OUTPUT_PATH = Path("data/processed/entrance_be_nl.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/entrance_be_nl_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    raw = row.get("options")
    if not isinstance(raw, list):
        return tuple()
    return tuple(str(option).strip() for option in raw if str(option).strip())


def main() -> None:
    """Extract Dutch-language Belgian entrance questions into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="entrance-be-nl-demo-1",
                language="nl",
                country="BE",
                dataset_name=DATASET_NAME,
                task=MEDICAL_ENTRANCE_MCQ.name,
                source_type="physician and dentist entrance examination",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="Unknown on dataset card; derived from public official exam questions",
                split="demo",
                question="'Vaccineren' betekent het toedienen van",
                options=("een antigeen", "een antibioticum", "een analgeticum", "een antihistaminicum"),
                label="een antigeen",
                specialty="generic competencies",
                exam_name="Toelatingsexamen Arts/Tandarts",
                native_or_translated="native",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{DEMO_OUTPUT_PATH}"
        )
        return

    for split_name in ("train", "dev", "test"):
        dataset = load_dataset(DATASET_ID, split=split_name)
        for row in dataset:
            if str(row.get("language", "")).strip().lower() != "nl":
                continue

            question = str(row.get("question", "")).strip()
            options = _safe_options(row)
            label = label_from_one_based_index(str(row.get("answer", "")), options)
            if not question or len(options) < 2 or label is None:
                continue

            category = str(row.get("category_original_lang", "")).strip() or None
            file_name = str(row.get("file_name", "")).strip() or "Belgian entrance exam"

            records.append(
                DatasetRecord(
                    id=f"entrance-be-nl-{split_name}-{row.get('original_question_num', len(records))}",
                    language="nl",
                    country="BE",
                    dataset_name=DATASET_NAME,
                    task=MEDICAL_ENTRANCE_MCQ.name,
                    source_type="physician and dentist entrance examination",
                    source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                    license="Unknown on dataset card; derived from public official exam questions",
                    split=split_name,
                    question=question,
                    options=options,
                    label=label,
                    specialty=category,
                    exam_name=file_name,
                    native_or_translated="native",
                )
            )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
