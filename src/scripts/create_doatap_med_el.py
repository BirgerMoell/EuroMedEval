"""Build a normalized JSONL file from the Greek DOATAP medical MCQ dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


DATASET_ID = "ilsp/medical_mcqa_greek"
OUTPUT_PATH = Path("data/processed/doatap_med_el.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/doatap_med_el_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    raw = row.get("multiple_choice_targets")
    if not isinstance(raw, list):
        return tuple()
    return tuple(str(option).strip() for option in raw if str(option).strip())


def _safe_label(row: dict, options: tuple[str, ...]) -> str | None:
    targets = row.get("targets")
    if isinstance(targets, list) and targets:
        target = str(targets[0]).strip()
        if target in options:
            return target

    scores = row.get("multiple_choice_scores")
    if isinstance(scores, list):
        for index, score in enumerate(scores):
            if int(score) == 1 and index < len(options):
                return options[index]
    return None


def main() -> None:
    """Extract Greek DOATAP questions into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="doatap-med-el-demo-1",
                language="el",
                country="GR",
                dataset_name="doatap-med-el",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="medical recognition exam MCQ",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY-NC-SA 4.0",
                split="demo",
                question="Η πρόσθια επιφάνεια του σώματος της μήτρας έρχεται σε σχέση με:",
                options=(
                    "Α. Τον ηβοκυστικό σύνδεσμο",
                    "Β. Τις εντερικές έλικες",
                    "Γ. Την ουροδόχο κύστη",
                    "Δ. Όλα τα παραπάνω",
                    "Ε. Κανένα από τα παραπάνω",
                ),
                label="Γ. Την ουροδόχο κύστη",
                specialty="anatomy",
                exam_name="DOATAP",
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
        question = str(row.get("inputs", "")).strip()
        options = _safe_options(row)
        label = _safe_label(row, options)
        if not question or len(options) < 2 or label is None:
            continue

        records.append(
            DatasetRecord(
                id=f"doatap-med-el-{row.get('idx', len(records))}",
                language="el",
                country="GR",
                dataset_name="doatap-med-el",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="medical recognition exam MCQ",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY-NC-SA 4.0",
                split="train",
                question=question,
                options=options,
                label=label,
                specialty=str(row.get("subject", "")).strip() or None,
                exam_name="DOATAP",
                native_or_translated="native",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
