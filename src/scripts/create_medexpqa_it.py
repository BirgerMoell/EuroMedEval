"""Build a normalized JSONL file from MedExpQA Italian."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import CLINICAL_CASE_MCQ


DATASET_ID = "HiTZ/MedExpQA"
DATASET_NAME = "medexpqa-it"
OUTPUT_PATH = Path("data/processed/medexpqa_it.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/medexpqa_it_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    raw = row.get("options")
    if not isinstance(raw, dict):
        return tuple()
    options = []
    for index in range(1, 6):
        value = raw.get(str(index))
        if value is None:
            continue
        text = str(value).strip()
        if text:
            options.append(f"{index}. {text}")
    return tuple(options)


def main() -> None:
    """Extract MedExpQA Italian into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="medexpqa-it-demo-1",
                language="it",
                country="IT",
                dataset_name=DATASET_NAME,
                task=CLINICAL_CASE_MCQ.name,
                source_type="multilingual medical exam QA anchor benchmark",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY 4.0",
                split="demo",
                question="Quale pensate sia la migliore risposta di Juan?",
                context="Juan, specializzando al secondo anno, assiste Sofia, una ragazza di 15 anni.",
                options=(
                    "1. Accettare la richiesta di amicizia perché non c'è nulla di inappropriato nella sua pagina.",
                    "2. Accettarla ma limitare l'accesso a parte dei contenuti.",
                    "3. Spiegare che è importante mantenere limiti professionali e non accettare la richiesta.",
                    "4. Dirle di fare la richiesta ma di non accettarla.",
                ),
                label="3. Spiegare che è importante mantenere limiti professionali e non accettare la richiesta.",
                specialty="ethics",
                exam_name="MedExpQA",
                native_or_translated="translated",
                notes="Bronze multilingual anchor derived from parallel CasiMedicos material.",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{DEMO_OUTPUT_PATH}"
        )
        return

    for split_name in ("train", "validation", "test"):
        dataset = load_dataset(DATASET_ID, "it", split=split_name)
        for row in dataset:
            question = str(row.get("question", "")).strip()
            context = str(row.get("full_question", "")).strip() or None
            options = _safe_options(row)
            correct_option = int(row.get("correct_option", 0))
            label = f"{correct_option}. {str(row.get('options', {}).get(str(correct_option), '')).strip()}"
            if not question or len(options) < 2 or label not in options:
                continue

            records.append(
                DatasetRecord(
                    id=f"medexpqa-it-{split_name}-{row.get('id', len(records))}",
                    language="it",
                    country="IT",
                    dataset_name=DATASET_NAME,
                    task=CLINICAL_CASE_MCQ.name,
                    source_type="multilingual medical exam QA anchor benchmark",
                    source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                    license="CC BY 4.0",
                    split=split_name,
                    question=question,
                    context=context,
                    options=options,
                    label=label,
                    exam_name="MedExpQA",
                    native_or_translated="translated",
                    notes="Bronze multilingual anchor derived from parallel CasiMedicos material.",
                )
            )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
