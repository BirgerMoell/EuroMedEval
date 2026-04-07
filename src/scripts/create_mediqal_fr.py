"""Build a normalized JSONL file from the MediQAl French clinical MCQ dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.source_parsers import label_from_answer_letter
from euromedeval.tasks import CLINICAL_CASE_MCQ


DATASET_ID = "ANR-MALADES/MediQAl"
DATASET_NAME = "mediqal-fr"
OUTPUT_PATH = Path("data/processed/mediqal_fr.jsonl")
DEMO_OUTPUT_PATH = Path("data/processed/mediqal_fr_demo.jsonl")


def _safe_options(row: dict) -> tuple[str, ...]:
    options = []
    for letter in ("a", "b", "c", "d", "e"):
        value = str(row.get(f"answer_{letter}", "")).strip()
        if value:
            options.append(f"{letter.upper()}. {value}")
    return tuple(options)


def main() -> None:
    """Extract MediQAl MCQU records into the EuroMedEval schema."""
    records: list[DatasetRecord] = []

    try:
        from datasets import load_dataset
    except ImportError:
        records.append(
            DatasetRecord(
                id="mediqal-fr-demo-1",
                language="fr",
                country="FR",
                dataset_name=DATASET_NAME,
                task=CLINICAL_CASE_MCQ.name,
                source_type="French medical examination clinical-case MCQ",
                source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                license="CC BY 4.0",
                split="demo",
                question="Au sujet des vaccinations :",
                context="Monsieur R. âgé de 37 ans, forestier, doit partir travailler pendant 2 ans au Gabon.",
                options=(
                    "A. Le vaccin contre la fièvre jaune est obligatoire",
                    "B. Le vaccin contre la fièvre jaune peut se faire au cabinet du médecin traitant",
                    "C. Le vaccin contre le choléra est un vaccin qui assure une protection supérieure à 80%",
                    "D. Le vaccin contre l'hépatite B est conseillé mais il ne se trouve pas en pharmacie, il faut contacter l'hôpital",
                    "E. Les vaccinations contre le tétanos et la poliomyélite ne sont pas indispensables",
                ),
                label="A. Le vaccin contre la fièvre jaune est obligatoire",
                specialty="Infectious Diseases",
                exam_name="MediQAl MCQU",
                native_or_translated="native",
            )
        )
        write_records_to_jsonl(records=records, output_path=DEMO_OUTPUT_PATH)
        print(
            "datasets package is required for full extraction. Wrote demo record to "
            f"{DEMO_OUTPUT_PATH}"
        )
        return

    for split_name in ("train", "validation", "test"):
        dataset = load_dataset(DATASET_ID, "mcqu", split=split_name)
        for row in dataset:
            question = str(row.get("question", "")).strip()
            context = str(row.get("clinical_case", "")).strip() or None
            options = _safe_options(row)
            label = label_from_answer_letter(str(row.get("correct_answers", "")), options)
            if not question or len(options) < 2 or label is None:
                continue

            records.append(
                DatasetRecord(
                    id=f"mediqal-fr-{split_name}-{row.get('id', len(records))}",
                    language="fr",
                    country="FR",
                    dataset_name=DATASET_NAME,
                    task=CLINICAL_CASE_MCQ.name,
                    source_type="French medical examination clinical-case MCQ",
                    source_url=f"https://huggingface.co/datasets/{DATASET_ID}",
                    license="CC BY 4.0",
                    split=split_name,
                    question=question,
                    context=context,
                    options=options,
                    label=label,
                    specialty=str(row.get("medical_subject", "")).strip() or None,
                    difficulty=str(row.get("question_type", "")).strip() or None,
                    exam_name="MediQAl MCQU",
                    native_or_translated="native",
                )
            )

    write_records_to_jsonl(records=records, output_path=OUTPUT_PATH)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
