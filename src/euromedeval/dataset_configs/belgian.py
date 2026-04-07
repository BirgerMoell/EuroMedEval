"""Belgian dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_ENTRANCE_MCQ


BELGIAN_DATASET_CONFIGS = [
    DatasetConfig(
        name="entrance-be-nl",
        pretty_name="Belgian Physician Entrance Exam (Dutch)",
        language="nl",
        country="BE",
        task=MEDICAL_ENTRANCE_MCQ.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/jjzha/belgian-entrance-exam-physician",
        source_type="physician and dentist entrance examination",
        license="Unknown on dataset card; derived from public official exam questions",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_entrance_be_nl.py",
        description="Dutch-language Belgian physician entrance exam questions reconstructed from public official exam archives.",
        notes="This is an entrance track and should be reported separately from physician qualification benchmarks.",
    ),
]
