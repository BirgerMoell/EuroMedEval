"""Build a normalized JSONL file from the Polish LDEK exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_answer_letter, parse_inline_lettered_mcq
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


DATASET_ID = "amu-cai/medical-exams-LDEK-PL-2008-2024"
DATASET_NAME = "ldek-pl"
OUTPUT_PATH = Path("data/processed/ldek_pl.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/ldek_pl_demo.jsonl")
PRETTY_SOURCE = "dental final examination"


def main() -> None:
    """Extract LDEK questions into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="ldek-pl-demo-1",
                language="pl",
                country="PL",
                dataset_name=DATASET_NAME,
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type=PRETTY_SOURCE,
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="See upstream source and CEM terms",
                split="demo",
                question="Wskaż prawidłowe stwierdzenie dotyczące torbieli gałeczkowo-szczękowej.",
                options=(
                    "A. Jest niezębopochodna",
                    "B. Jest zębopochodna",
                    "C. Częściej umiejscawia się od strony podniebienia",
                    "D. Może powodować bóle na skutek ucisku nerwu nosowo-podniebiennego",
                    "E. Cień w RTG odpowiadający torbieli nie łączy się z ozębną",
                ),
                label="D. Może powodować bóle na skutek ucisku nerwu nosowo-podniebiennego",
                exam_name="LDEK",
                specialty="dentistry",
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
        exam_name = str(row.get("edition", "")).strip() or "LDEK"

        records.append(
            DatasetRecord(
                id=f"ldek-pl-{row.get('edition', 'unk')}-{row.get('question_id', len(records))}",
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
                specialty="dentistry",
                exam_name=exam_name,
                native_or_translated="native",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
