"""Build a normalized JSONL file from the Italian Test Medicina dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def _extract_question(row: dict) -> str:
    for key in ("question", "prompt", "query"):
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def _extract_options(row: dict) -> tuple[str, ...]:
    for key in ("options", "choices", "answers"):
        value = row.get(key)
        if isinstance(value, list):
            cleaned = [str(item).strip() for item in value if str(item).strip()]
            if cleaned:
                return tuple(cleaned)
        if isinstance(value, dict):
            cleaned = [str(item).strip() for item in value.values() if str(item).strip()]
            if cleaned:
                return tuple(cleaned)
    return tuple()


def _extract_label(row: dict, options: tuple[str, ...]) -> str:
    for key in ("answer", "correct_answer", "label_text"):
        value = row.get(key)
        if value and str(value).strip() in options:
            return str(value).strip()

    for key in ("label", "answer_idx", "correct_option"):
        value = row.get(key)
        if value is None:
            continue
        try:
            index = int(value)
        except (TypeError, ValueError):
            continue
        if 0 <= index < len(options):
            return options[index]
        if 1 <= index <= len(options):
            return options[index - 1]
    return ""


def main() -> None:
    """Write a small reproducible subset from Test Medicina."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        output_path = Path("data/processed/test_medicina_demo.jsonl")
        records.append(
            DatasetRecord(
                id="test-medicina-demo-1",
                language="it",
                country="IT",
                dataset_name="medschool-test-it",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="Italian national medical school entrance exam MCQ",
                source_url="https://huggingface.co/datasets/room-b007/test-medicina",
                license="Apache-2.0",
                split="demo",
                question="Quale dei seguenti reperti suggerisce maggiormente una meningite batterica?",
                options=("Rigidita nucale", "Dolore al tallone", "Prurito lieve", "Miopia"),
                label="Rigidita nucale",
            )
        )
        write_records_to_jsonl(records=records, output_path=output_path)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{output_path}"
        )
        return

    dataset = load_dataset("room-b007/test-medicina", split="train")
    limit = min(3000, len(dataset))

    for idx in range(limit):
        row = dataset[idx]
        question = _extract_question(row)
        options = _extract_options(row)
        label = _extract_label(row, options)

        if not question or len(options) < 2 or not label:
            continue
        if label not in options:
            continue

        records.append(
            DatasetRecord(
                id=f"test-medicina-it-{idx}",
                language="it",
                country="IT",
                dataset_name="medschool-test-it",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="Italian national medical school entrance exam MCQ",
                source_url="https://huggingface.co/datasets/room-b007/test-medicina",
                license="Apache-2.0",
                split="train",
                question=question,
                options=options,
                label=label,
            )
        )

    output_path = Path("data/processed/test_medicina.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
