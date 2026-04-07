"""Norwegian dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


NORWEGIAN_DATASET_CONFIGS = [
    DatasetConfig(
        name="normedqa-no",
        pretty_name="NorMedQA",
        language="no",
        country="NO",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.OFFICIAL,
        source_url="https://huggingface.co/datasets/SimulaMet/NorMedQA",
        source_type="medical question answering from Norwegian exam sources",
        license="CC BY 4.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_nor_medqa.py",
        description=(
            "Norwegian medical QA dataset curated from public exam materials, "
            "distributed with CC BY 4.0 terms."
        ),
    ),
]

