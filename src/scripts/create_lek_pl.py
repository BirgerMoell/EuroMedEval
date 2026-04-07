"""Template script for creating a Polish medical exam dataset."""

from __future__ import annotations

from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def main() -> None:
    """Write a tiny example dataset in the normalized schema.

    Replace this with a real parser once a source and license have been confirmed.
    """
    records = [
        DatasetRecord(
            id="lek-pl-demo-1",
            language="pl",
            country="PL",
            dataset_name="lek-pl",
            task=MEDICAL_KNOWLEDGE_MCQ.name,
            source_type="medical licensing exam",
            source_url="https://www.gov.pl/",
            license="TBD per source",
            split="demo",
            question="Który z poniższych objawów najbardziej sugeruje zapalenie opon mózgowo-rdzeniowych?",
            options=("Sztywność karku", "Katar", "Ból pięty", "Świąd skóry"),
            label="Sztywność karku",
            exam_name="demo",
            native_or_translated="native",
        )
    ]
    output_path = Path("data/processed/lek_pl_demo.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()

