"""Polish dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


POLISH_DATASET_CONFIGS = [
    DatasetConfig(
        name="lek-pl",
        pretty_name="Polish LEK-style Medical Exam",
        language="pl",
        country="PL",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://www.gov.pl/",
        source_type="medical licensing exam",
        license="TBD per source",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_lek_pl.py",
        description="Starter config for a Polish native medical licensing dataset.",
        notes="This is a scaffold entry and should be refined once a legally clear source is confirmed.",
    ),
]

