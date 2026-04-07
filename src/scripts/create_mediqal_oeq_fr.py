"""Build a normalized JSONL file from the MediQAl French open-ended QA dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, RecordFormat, write_records_to_jsonl
from euromedeval.tasks import CLINICAL_CASE_QA


DATASET_ID = "ANR-MALADES/MediQAl"
DATASET_NAME = "mediqal-oeq-fr"
OUTPUT_PATH = Path("data/processed/mediqal_oeq_fr.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/mediqal_oeq_fr_demo.jsonl")


def main() -> None:
    """Extract MediQAl open-ended records into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="mediqal-oeq-fr-demo-1",
                language="fr",
                country="FR",
                dataset_name=DATASET_NAME,
                task=CLINICAL_CASE_QA.name,
                source_type="French medical examination open-ended case QA",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY 4.0",
                split="demo",
                question="Quels sont éléments de gravité au moment de l’arrivée du patient ?",
                context="Homme, 58 ans, majoration de dyspnée chez un BPCO connu depuis 20 ans.",
                answers=(
                    "FC>125bpm; terrain BPCO; SpO2<90%; FR>30/min; sueurs; cyanose; tirage; signes d’insuffisance droite.",
                ),
                record_format=RecordFormat.GENERATIVE_QA,
                specialty="Emergency Medicine",
                difficulty="Reasoning",
                exam_name="MediQAl OEQ",
                native_or_translated="native",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{DEMO_OUTPUT_PATH}"
        )
        return

    dataset = load_dataset(DATASET_ID, "oeq", split="test")
    for row in dataset:
        question = str(row.get("question", "")).strip()
        context = str(row.get("clinical_case", "")).strip() or None
        answer = str(row.get("answer", "")).strip()
        if not question or not answer:
            continue

        records.append(
            DatasetRecord(
                id=f"mediqal-oeq-fr-test-{row.get('id', len(records))}",
                language="fr",
                country="FR",
                dataset_name=DATASET_NAME,
                task=CLINICAL_CASE_QA.name,
                source_type="French medical examination open-ended case QA",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY 4.0",
                split="test",
                question=question,
                context=context,
                answers=(answer,),
                record_format=RecordFormat.GENERATIVE_QA,
                specialty=str(row.get("medical_subject", "")).strip() or None,
                difficulty=str(row.get("question_type", "")).strip() or None,
                exam_name="MediQAl OEQ",
                native_or_translated="native",
            )
        )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
