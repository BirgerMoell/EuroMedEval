"""Build a normalized JSONL file from the Italian MIUR clinical state exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_answer_letter
from euromedeval.tasks import CLINICAL_CASE_MCQ


DATASET_ID = "Detsutut/miur-medicina-clinica"
DATASET_NAME = "miur-clinica-it"
OUTPUT_PATH = Path("data/processed/miur_clinica_it.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/miur_clinica_it_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    options = []
    for letter in ("A", "B", "C", "D", "E"):
        value = str(row.get(f"Opzione {letter}", "")).strip()
        if value:
            options.append(f"{letter}. {value}")
    return tuple(options)


def main() -> None:
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="miur-clinica-it-demo-1",
                language="it",
                country="IT",
                dataset_name=DATASET_NAME,
                task=CLINICAL_CASE_MCQ.name,
                source_type="physician state exam clinical-area MCQ",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="Apache-2.0",
                split="demo",
                question="Qual è la condotta più appropriata nel sospetto di appendicite acuta?",
                options=(
                    "A. Dimissione con follow-up domiciliare",
                    "B. Valutazione chirurgica urgente",
                    "C. Solo terapia antibiotica orale",
                    "D. Nessun approfondimento",
                    "E. Ripetere il controllo tra 6 mesi",
                ),
                label="B. Valutazione chirurgica urgente",
                specialty="Chirurgia Generale",
                exam_name="MIUR area clinica",
                native_or_translated="native",
                notes="Full dataset requires accepted access terms on Hugging Face.",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(f"datasets package is required for full extraction. Wrote demo record to {DEMO_OUTPUT_PATH}")
        return

    for split_name in ("train", "test"):
        dataset = load_dataset(DATASET_ID, split=split_name)
        for row in dataset:
            question = str(row.get("Domanda", "")).strip()
            options = _safe_options(row)
            label = label_from_answer_letter(str(row.get("Risposta", "")), options)
            if not question or len(options) < 2 or label is None:
                continue
            records.append(
                DatasetRecord(
                    id=f"miur-clinica-it-{split_name}-{row.get('Id', len(records))}",
                    language="it",
                    country="IT",
                    dataset_name=DATASET_NAME,
                    task=CLINICAL_CASE_MCQ.name,
                    source_type="physician state exam clinical-area MCQ",
                    source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                    license="Apache-2.0",
                    split=split_name,
                    question=question,
                    options=options,
                    label=label,
                    specialty=str(row.get("Topic", "")).strip() or None,
                    exam_name="MIUR area clinica",
                    native_or_translated="native",
                    notes="Full dataset requires accepted access terms on Hugging Face.",
                )
            )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
