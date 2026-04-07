"""Albanian dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_ENTRANCE_MCQ


ALBANIAN_DATASET_CONFIGS = [
    DatasetConfig(
        name="entrance-al-sq",
        pretty_name="Albanian Medical Entrance Exam",
        language="sq",
        country="AL",
        task=MEDICAL_ENTRANCE_MCQ.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/marjpri/albanian-medical-exams-cycles-mcq-190",
        source_type="digital medical entrance examination",
        license="Derived from public official exam material on QSHA",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_entrance_al_sq.py",
        description="Albanian multiple-choice questions from the official digital medicine entrance exam pool.",
        notes="This is an entrance track sourced from QSHA and should not be pooled with physician licensing exams.",
    ),
]
