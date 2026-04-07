from euromedeval.benchmarker import Benchmarker, aggregate_language_scores
from euromedeval.schemas import DatasetRecord
from euromedeval.tasks import MEDICAL_KNOWLEDGE_MCQ


def test_score_mcq_returns_accuracy_and_ci() -> None:
    records = [
        DatasetRecord(
            id="1",
            language="sv",
            country="SE",
            dataset_name="demo",
            task=MEDICAL_KNOWLEDGE_MCQ.name,
            source_type="exam",
            source_url="https://example.com",
            license="test",
            split="test",
            question="Q1",
            options=("A", "B", "C", "D"),
            label="A",
        ),
        DatasetRecord(
            id="2",
            language="sv",
            country="SE",
            dataset_name="demo",
            task=MEDICAL_KNOWLEDGE_MCQ.name,
            source_type="exam",
            source_url="https://example.com",
            license="test",
            split="test",
            question="Q2",
            options=("A", "B", "C", "D"),
            label="B",
        ),
    ]

    benchmarker = Benchmarker(bootstrap_iterations=50, seed=1)
    score = benchmarker.score_mcq(
        dataset_name="demo",
        language="sv",
        task=MEDICAL_KNOWLEDGE_MCQ.name,
        native=True,
        records=records,
        predictions={"1": "A", "2": "C"},
    )

    assert score.accuracy == 0.5
    assert 0.0 <= score.ci_low <= score.ci_high <= 1.0


def test_aggregate_language_scores_is_native_only_and_task_weighted() -> None:
    scores = [
        benchmark_score(dataset_name="a", task="medical-knowledge-mcq", accuracy=0.8, native=True),
        benchmark_score(dataset_name="b", task="medical-knowledge-mcq", accuracy=0.6, native=True),
        benchmark_score(dataset_name="c", task="clinical-case-mcq", accuracy=0.5, native=True),
        benchmark_score(dataset_name="d", task="evidence-qa", accuracy=0.9, native=False),
    ]
    summary = aggregate_language_scores(scores)
    assert summary["num_native_datasets"] == 3.0
    assert round(summary["native_task_weighted_accuracy"], 4) == 0.6


def benchmark_score(*, dataset_name: str, task: str, accuracy: float, native: bool):
    from euromedeval.benchmarker import DatasetScore

    return DatasetScore(
        dataset_name=dataset_name,
        language="sv",
        task=task,
        native=native,
        accuracy=accuracy,
        ci_low=max(0.0, accuracy - 0.1),
        ci_high=min(1.0, accuracy + 0.1),
        sample_size=10,
    )

