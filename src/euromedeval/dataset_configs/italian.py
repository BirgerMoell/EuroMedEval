"""Italian dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


ITALIAN_DATASET_CONFIGS = [
    DatasetConfig(
        name="medschool-test-it",
        pretty_name="Medical School Entrance Exam (Italy)",
        language="it",
        country="IT",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/room-b007/test-medicina",
        source_type="national medical school entrance exam MCQ",
        license="Apache 2.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_test_medicina.py",
        description=(
            "Italian national medical school exam questions with broader subject coverage "
            "including medical-school core science topics and general knowledge."
        ),
        notes=(
            "Included as silver native dataset because it includes non-clinical "
            "sections and is not strictly clinician-grade medical Q&A."
        ),
    ),
]

