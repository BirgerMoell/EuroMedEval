"""French dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import CLINICAL_CASE_MCQ, MEDICAL_KNOWLEDGE_MCQ


FRENCH_DATASET_CONFIGS = [
    DatasetConfig(
        name="frenchmedmcqa-fr",
        pretty_name="FrenchMedMCQA (single-answer subset)",
        language="fr",
        country="FR",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/qanastek/frenchmedmcqa",
        source_type="medical multiple-choice questions from French pharmacy specialization exams",
        license="Apache-2.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_french_medmcqa.py",
        description=(
            "Single-answer subset of French medical MCQ items from FrenchMedMCQA with "
            "the option fields mapped to a uniform schema for direct scoring."
        ),
        notes=(
            "This config intentionally filters to single-answer questions first; "
            "other items can be added in a follow-up multi-answer track."
        ),
    ),
    DatasetConfig(
        name="mediqal-fr",
        pretty_name="MediQAl (French clinical MCQ)",
        language="fr",
        country="FR",
        task=CLINICAL_CASE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.OFFICIAL,
        source_url="https://huggingface.co/datasets/ANR-MALADES/MediQAl",
        source_type="French medical examination clinical-case MCQ",
        license="CC BY 4.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_mediqal_fr.py",
        description="French medical examination benchmark with clinical cases and single-answer MCQ items from MediQAl.",
        notes="Current export uses the MCQU subset; MCQM and OEQ can be added as dedicated tracks later.",
    ),
]
