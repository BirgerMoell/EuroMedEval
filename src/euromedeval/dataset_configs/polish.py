"""Polish dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


POLISH_DATASET_CONFIGS = [
    DatasetConfig(
        name="lek-pl",
        pretty_name="Polish LEK Medical Final Examination",
        language="pl",
        country="PL",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/amu-cai/medical-exams-LEK-PL-2008-2024",
        source_type="medical final examination",
        license="See upstream source and CEM terms",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_lek_pl.py",
        description="Polish LEK exam questions scraped from official CEM sources and normalized for local evaluation.",
        notes="Dataset card states it was scraped from CEM and excludes image-based and outdated questions.",
    ),
    DatasetConfig(
        name="ldek-pl",
        pretty_name="Polish LDEK Dental Final Examination",
        language="pl",
        country="PL",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/amu-cai/medical-exams-LDEK-PL-2008-2024",
        source_type="dental final examination",
        license="See upstream source and CEM terms",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_ldek_pl.py",
        description="Polish LDEK dentist licensing questions reconstructed from public exam archives.",
        notes="Best treated as a dentistry-specific leaderboard track within Poland.",
    ),
    DatasetConfig(
        name="pes-pl",
        pretty_name="Polish PES Specialist Board Exams",
        language="pl",
        country="PL",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/amu-cai/medical-exams-PES-PL-2007-2024",
        source_type="specialist board certification exam",
        license="See upstream source and CEM terms",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_pes_pl.py",
        description="Polish specialist board certification questions spanning many specialties and exam years.",
        notes="Large specialist exam resource suitable for specialty-aware reporting instead of a single pooled score.",
    ),
]
