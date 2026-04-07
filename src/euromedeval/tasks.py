"""Task definitions for EuroMedEval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskDefinition:
    """A benchmark task family."""

    name: str
    pretty_name: str
    description: str


MEDICAL_KNOWLEDGE_MCQ = TaskDefinition(
    name="medical-knowledge-mcq",
    pretty_name="Medical Knowledge MCQ",
    description="Multiple-choice questions from licensing, residency, or specialist exams.",
)

MEDICAL_ENTRANCE_MCQ = TaskDefinition(
    name="medical-entrance-mcq",
    pretty_name="Medical Entrance MCQ",
    description="Multiple-choice questions from physician or medical-school entrance examinations.",
)

CLINICAL_CASE_MCQ = TaskDefinition(
    name="clinical-case-mcq",
    pretty_name="Clinical Case MCQ",
    description="Case-based questions such as diagnosis, urgency, or next best step.",
)

EVIDENCE_QA = TaskDefinition(
    name="evidence-qa",
    pretty_name="Evidence QA",
    description="Medical literature or guideline-based question answering.",
)

ALL_TASKS = {
    MEDICAL_KNOWLEDGE_MCQ.name: MEDICAL_KNOWLEDGE_MCQ,
    MEDICAL_ENTRANCE_MCQ.name: MEDICAL_ENTRANCE_MCQ,
    CLINICAL_CASE_MCQ.name: CLINICAL_CASE_MCQ,
    EVIDENCE_QA.name: EVIDENCE_QA,
}
