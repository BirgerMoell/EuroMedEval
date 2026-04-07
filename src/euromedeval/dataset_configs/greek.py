"""Greek dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


GREEK_DATASET_CONFIGS = [
    DatasetConfig(
        name="doatap-med-el",
        pretty_name="Greek DOATAP Medical MCQ",
        language="el",
        country="GR",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.OFFICIAL,
        source_url="https://huggingface.co/datasets/ilsp/medical_mcqa_greek",
        source_type="medical recognition exam MCQ",
        license="CC BY-NC-SA 4.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_doatap_med_el.py",
        description="Greek medical multiple-choice questions extracted from DOATAP exam material.",
        notes="Curated by ILSP/Athena RC from past exams published by the Hellenic recognition authority.",
    ),
]
