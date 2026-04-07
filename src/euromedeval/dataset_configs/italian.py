"""Italian dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import CLINICAL_CASE_MCQ, MEDICAL_KNOWLEDGE_MCQ


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
    DatasetConfig(
        name="medexpqa-it",
        pretty_name="MedExpQA Italian Anchor",
        language="it",
        country="IT",
        task=CLINICAL_CASE_MCQ.name,
        tier=DatasetTier.BRONZE,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/HiTZ/MedExpQA",
        source_type="multilingual medical exam QA anchor benchmark",
        license="CC BY 4.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=False,
        clinically_reviewed=False,
        creation_script="src/scripts/create_medexpqa_it.py",
        description="Italian MedExpQA anchor set derived from multilingual MIR-style exam material with gold explanations.",
        notes="Parallel multilingual anchor resource; keep separate from native-first flagship aggregates.",
    ),
]
