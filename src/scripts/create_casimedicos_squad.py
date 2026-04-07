"""Build a normalized JSONL file from CasiMedicos SQuAD."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, RecordFormat, write_records_to_jsonl
from euromedeval.tasks import EVIDENCE_QA


def _extract_answers(row: dict) -> tuple[str, ...]:
    payload = row.get("answers")
    if isinstance(payload, dict):
        text_values = payload.get("text")
        if isinstance(text_values, list):
            cleaned = [str(item).strip() for item in text_values if str(item).strip()]
            if cleaned:
                return tuple(cleaned)
    if isinstance(payload, list):
        cleaned = [str(item).strip() for item in payload if str(item).strip()]
        if cleaned:
            return tuple(cleaned)
    answer = row.get("answer")
    if answer and str(answer).strip():
        return (str(answer).strip(),)
    return tuple()


def main() -> None:
    """Write a reproducible subset from CasiMedicos in extractive QA format."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        output_path = Path("data/processed/casimedicos_squad_demo.jsonl")
        records.append(
            DatasetRecord(
                id="casimedicos-es-demo-1",
                language="es",
                country="ES",
                dataset_name="casimedicos-es",
                task=EVIDENCE_QA.name,
                source_type="clinical question answering from MIR-style medical questions",
                source_url="https://huggingface.co/datasets/HiTZ/casimedicos-squad",
                license="CC BY 4.0",
                split="demo",
                question="Cual es el tratamiento inicial recomendado en una anafilaxia grave?",
                context="Paciente con urticaria, hipotension y disnea tras exposicion a un alergen.",
                record_format=RecordFormat.EXTRACTIVE_QA,
                answers=("adrenalina intramuscular",),
                native_or_translated="native",
            )
        )
        write_records_to_jsonl(records=records, output_path=output_path)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{output_path}"
        )
        return

    dataset = load_dataset("HiTZ/casimedicos-squad", split="train")
    limit = min(3000, len(dataset))

    for idx in range(limit):
        row = dataset[idx]
        question = str(row.get("question", "")).strip()
        context = str(row.get("context", "")).strip()
        answers = _extract_answers(row)
        if not question or not context or not answers:
            continue

        records.append(
            DatasetRecord(
                id=f"casimedicos-es-{idx}",
                language="es",
                country="ES",
                dataset_name="casimedicos-es",
                task=EVIDENCE_QA.name,
                source_type="clinical question answering from MIR-style medical questions",
                source_url="https://huggingface.co/datasets/HiTZ/casimedicos-squad",
                license="CC BY 4.0",
                split="train",
                question=question,
                context=context,
                record_format=RecordFormat.EXTRACTIVE_QA,
                answers=answers,
                native_or_translated="native",
            )
        )

    output_path = Path("data/processed/casimedicos_squad.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
