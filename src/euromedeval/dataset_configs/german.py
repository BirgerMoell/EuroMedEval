"""German dataset configs."""

from __future__ import annotations

from ..schemas import AccessMode, DatasetConfig, DatasetStatus, DatasetTier
from ..tasks import MEDICAL_KNOWLEDGE_MCQ


GERMAN_DATASET_CONFIGS = [
    DatasetConfig(
        name="impp-sample-de",
        pretty_name="IMPP Medizin Beispielaufgaben",
        language="de",
        country="DE",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        tier=DatasetTier.SILVER,
        status=DatasetStatus.OFFICIAL,
        source_url="https://www.impp.de/pruefungen/medizin/beispielaufgaben.html",
        source_type="official state exam sample questions",
        license="Copyrighted official sample tasks; use subject to IMPP terms",
        access_mode=AccessMode.PERMISSIONED,
        native=True,
        clinically_reviewed=False,
        creation_script="src/scripts/create_impp_sample_de.py",
        description="German official sample questions from the IMPP medical state examination pages.",
        notes=(
            "Keep as a manual local-import track because the IMPP site explicitly restricts "
            "automated reuse and text/data mining."
        ),
    ),
]
