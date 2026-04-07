"""Build a normalized JSONL file from Swedish PubMedQA."""

from __future__ import annotations

import json
from pathlib import Path

from euromedeval.schemas import DatasetRecord, write_records_to_jsonl
from euromedeval.tasks import EVIDENCE_QA


SOURCE_PATH = (
    Path(__file__).resolve().parents[3]
    / "swedish-medical-benchmark"
    / "benchmarks/pubmedqa/data/ori_pqal_swe.json"
)

OPTIONS = ("ja", "nej", "kanske")


def main() -> None:
    """Write the migrated Swedish PubMedQA benchmark to JSONL."""
    raw_data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    records: list[DatasetRecord] = []

    for raw_id, row in raw_data.items():
        label = str(row["final_decision"]).strip().lower()
        if label not in OPTIONS:
            continue
        records.append(
            DatasetRecord(
                id=f"pubmedqa-sv-{raw_id}",
                language="sv",
                country="SE",
                dataset_name="pubmedqa-sv",
                task=EVIDENCE_QA.name,
                source_type="translated medical literature QA",
                source_url="https://github.com/BirgerMoell/swedish-medical-benchmark",
                license="See upstream dataset license",
                split="train",
                question=row["QUESTION"].strip(),
                context="\n\n".join(row.get("CONTEXTS", [])),
                options=OPTIONS,
                label=label,
                year=int(row["YEAR"]) if row.get("YEAR") else None,
                evidence_source="PubMed abstract",
                native_or_translated="translated",
                translation_method="legacy benchmark translation",
            )
        )

    output_path = Path("data/processed/pubmedqa_sv.jsonl")
    write_records_to_jsonl(records=records, output_path=output_path)
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
