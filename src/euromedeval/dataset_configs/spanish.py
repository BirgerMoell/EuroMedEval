"""Spanish dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier, RecordFormat
from ..tasks import EVIDENCE_QA, MEDICAL_KNOWLEDGE_MCQ


SPANISH_DATASET_CONFIGS = [
    DatasetConfig(
        name="head-qa-es",
        pretty_name="HEAD-QA Spanish Healthcare Exams",
        language="es",
        country="ES",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.GOLD,
        status=DatasetStatus.OFFICIAL,
        source_url="https://huggingface.co/datasets/dvilares/head_qa",
        source_type="healthcare specialist-position exam MCQ",
        license="MIT",
        access_mode=AccessMode.SCRIPT_ONLY,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_head_qa_es.py",
        description="Spanish healthcare professional exam questions converted to a unified MCQ format.",
    ),
    DatasetConfig(
        name="casimedicos-es",
        pretty_name="CasiMedicos Clinical QA",
        language="es",
        country="ES",
        task=EVIDENCE_QA.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.UNOFFICIAL,
        source_url="https://huggingface.co/datasets/HiTZ/casimedicos-squad",
        source_type="clinical question answering from MIR-style medical questions",
        license="CC BY 4.0",
        access_mode=AccessMode.SCRIPT_ONLY,
        record_format=RecordFormat.EXTRACTIVE_QA,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_casimedicos_squad.py",
        description="Spanish clinical QA set stored in extractive QA format.",
        notes="Enabled after adding non-MCQ record support and QA scoring.",
    ),
]
