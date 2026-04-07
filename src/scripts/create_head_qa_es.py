"""Build a normalized JSONL file from HEAD-QA (Spanish)."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def _safe_question(question: object) -> str:
    text = str(question) if question is not None else ""
    return text.strip()


def _safe_answers(row: dict) -> tuple[str, ...]:
    answers = row.get("answers")
    if isinstance(answers, list):
        normalized = [
            str(item.get("atext", item)).strip() for item in answers if isinstance(item, dict)
        ]
    elif isinstance(answers, dict):
        normalized = [str(v).strip() for v in answers.values() if str(v).strip()]
    else:
        normalized = []
    return tuple(option for option in normalized if option)


def _safe_label(row: dict, options: tuple[str, ...]) -> str:
    raw = row.get("ra")
    if raw is None:
        return ""
    try:
        index = int(str(raw).strip())
    except ValueError:
        return ""
    if 1 <= index <= len(options):
        return options[index - 1]
    return ""


def main() -> None:
    """Write a small reproducible sample from the Spanish HEAD-QA split."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        output_path = Path("data/processed/head_qa_es_demo.jsonl")
        records.append(
            DatasetRecord(
                id="head-qa-es-demo-1",
                language="es",
                country="ES",
                dataset_name="head-qa-es",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="healthcare specialist-position exam MCQ",
                source_url="https://huggingface.co/datasets/dvilares/head_qa",
                license="MIT",
                split="demo",
                question="Paciente de 58 años con dolor torácico irradiado. ¿Cuál es la conducta inicial más urgente?",
                options=("Activar código infarto", "Control de síntomas", "Alta inmediata", "No hacer nada"),
                label="Activar código infarto",
            )
        )
        write_records_to_jsonl(records, output_path)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{output_path}"
        )
        return

    dataset = load_dataset("dvilares/head_qa", "es", split="train")
    limit = min(2000, len(dataset))

    for idx in range(limit):
        row = dataset[idx]
        question = _safe_question(row.get("qtext", row.get("question")))
        options = _safe_answers(row)
        label = _safe_label(row, options)

        if not question or not options or not label:
            continue
        if label not in options:
            continue

        records.append(
            DatasetRecord(
                id=f"head-qa-es-{idx}",
                language="es",
                country="ES",
                dataset_name="head-qa-es",
                task=MEDICAL_KNOWLEDGE_MCQ.name,
                source_type="healthcare specialist-position exam MCQ",
                source_url="https://huggingface.co/datasets/dvilares/head_qa",
                license="MIT",
                split="train",
                question=question,
                options=options,
                label=label,
            )
        )

    output_path = Path("data/processed/head_qa_es.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()

