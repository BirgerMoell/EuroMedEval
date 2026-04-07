# Methodology

## Core idea

EuroMedEval is designed as a **native-first medical benchmark** for Europe.

That means the benchmark should be strongest where existing benchmarks are weakest:

- local medical language
- real local exams
- local clinical reasoning patterns
- transparent provenance

## Dataset policy

We separate datasets into:

- `gold`: native, real medical data with clean provenance
- `silver`: native and clinically relevant, but less mature or less open
- `bronze`: translated anchor datasets

The main public language score should be driven by native datasets.

In practice, early EuroMedEval expansion should prioritize:

- national licensing or board-style exams
- residency entrance exams
- specialist exams
- medically reviewed educational banks with stable answer keys

Seed datasets from Norway, Spain, France, and Italy are now included as examples of this policy.

## Task policy

The initial focus is on automatically scorable tasks:

- medical knowledge MCQ
- clinical case MCQ
- evidence and literature QA

EuroMedEval now supports both MCQ-style records and QA-style records. MCQ datasets remain the main benchmark backbone, while extractive or generative QA can be added without being forced into answer-option form.

Free-text and clinician-graded tasks are valuable, but should come later once the contributor base is strong enough to support them.

## Scoring

Per-dataset MCQ evaluation uses:

- accuracy
- bootstrap resampling
- confidence intervals

QA-style datasets use exact match as the primary metric, token-level F1 as a secondary metric, and bootstrap confidence intervals on exact match.

Per-language scoring should:

- include native datasets only in the flagship score
- weight task families evenly
- report translated anchor datasets separately

## Reproducibility

Every public result should log:

- model identifier
- model date or version if available
- prompt template
- decoding settings
- dataset version
- evaluation date

## Limits

Strong MCQ performance does not imply clinical readiness.

This benchmark is intended as:

- a screening tool
- a comparison tool
- a transparency tool

It is not, by itself, evidence that a model is safe to deploy in clinical care.
