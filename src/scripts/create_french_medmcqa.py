"""Build a normalized JSONL file from FrenchMedMCQA."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def _pick_question(row: dict) -> str:
    for key in ("question", "query", "prompt"):
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def _pick_options(row: dict) -> tuple[str, ...]:
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


def _pick_label(row: dict, options: tuple[str, ...]) -> str:
    for key in ("answer", "label_text", "correct_answer"):
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
    """Write a small reproducible subset from FrenchMedMCQA."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        output_path = Path("data/processed/french_medmcqa_demo.jsonl")
        records.append(
            DatasetRecord(
                id="frenchmedmcqa-demo-1",
                language="fr",
                country="FR",
                dataset_name="frenchmedmcqa-fr",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="French pharmacy specialization exam MCQ",
                source_url="https://huggingface.co/datasets/qanastek/frenchmedmcqa",
                license="Apache-2.0",
                split="demo",
                question="Quel examen est le plus approprie pour confirmer une embolie pulmonaire suspectee ?",
                options=("Angioscanner thoracique", "ECG d'effort", "Radiographie du poignet", "Audiogramme"),
                label="Angioscanner thoracique",
            )
        )
        write_records_to_jsonl(records=records, output_path=output_path)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{output_path}"
        )
        return

    dataset = load_dataset("qanastek/frenchmedmcqa", split="train")
    limit = min(3000, len(dataset))

    for idx in range(limit):
        row = dataset[idx]
        question = _pick_question(row)
        options = _pick_options(row)
        label = _pick_label(row, options)

        if not question or len(options) < 2 or not label:
            continue
        if label not in options:
            continue

        records.append(
            DatasetRecord(
                id=f"frenchmedmcqa-fr-{idx}",
                language="fr",
                country="FR",
                dataset_name="frenchmedmcqa-fr",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="French pharmacy specialization exam MCQ",
                source_url="https://huggingface.co/datasets/qanastek/frenchmedmcqa",
                license="Apache-2.0",
                split="train",
                question=question,
                options=options,
                label=label,
            )
        )

    output_path = Path("data/processed/french_medmcqa.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
