# EuroMedEval

EuroMedEval is an open benchmark framework for evaluating language models on **real medical data across European languages**.

The project is deliberately **native-first**:

- native medical licensing exams
- residency entrance exams
- specialist certification questions
- clinically reviewed case vignettes

Translated benchmarks are still useful, but only as supporting anchor tasks. They should not define the flagship score.

## Why this project exists

Most medical LLM benchmarks are still dominated by English or by translated datasets. That is not enough for healthcare.

Medical language is local:

- terminology varies
- clinical practice varies
- exam formats vary
- safety expectations vary

EuroMedEval is designed to measure model performance in the medical contexts that people actually work in.

## Principles

- **Native-first**: real local datasets come before translated ones
- **Clinically grounded**: prioritize medical exams and case-based reasoning
- **Open and reproducible**: dataset provenance, scripts, and evaluation logic are public
- **Contributor-friendly**: adding a dataset should follow a stable template
- **Transparent scoring**: confidence intervals, prompts, and settings should be visible

## What is in this scaffold

- a normalized dataset schema
- a lightweight dataset registry
- a minimal benchmarker with bootstrap confidence intervals
- seed dataset configs for Albania, Belgium, Sweden, Greece, Norway, Spain, France, Italy, and Poland
- starter scripts for dataset ingestion
- contribution and dataset guides
- a build CLI for reconstructing datasets from local sources or Hugging Face

## Repository layout

```text
EuroMedEval/
├── src/
│   ├── euromedeval/
│   │   ├── benchmarker.py
│   │   ├── registry.py
│   │   ├── schemas.py
│   │   ├── tasks.py
│   │   └── dataset_configs/
│   └── scripts/
├── docs/
├── tests/
├── CONTRIBUTING.md
├── NEW_DATASET_GUIDE.md
└── pyproject.toml
```

## Quick start

```bash
cd /Users/birger/Documents/Papers/EuroMedEval
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m euromedeval list-datasets
python -m euromedeval list-datasets --language sv
python -m euromedeval build-dataset smdt-sv
python -m euromedeval build-all --language sv
```

Without installation, you can also run:

```bash
PYTHONPATH=src python3 -m euromedeval list-datasets
```

## Dataset philosophy

EuroMedEval uses three practical dataset tiers:

- `gold`: native-language, real medical data with clean provenance and public or approved redistribution
- `silver`: strong clinical relevance, but weaker redistribution or validation status
- `bronze`: translated anchor datasets

Only native datasets should drive the main public language score.

Entrance-exam datasets are still valuable, but they should live in their own benchmark track rather than be pooled into physician licensing or specialist certification aggregates.

Multilingual parallel resources are useful as comparison anchors, but they should stay in bronze support tracks rather than define the native-first flagship score.

## Initial roadmap

1. Make Swedish the reference language with migrated SMLB-style datasets.
2. Add founding languages with at least one native exam dataset each.
3. Launch native-only and all-dataset leaderboards separately.
4. Add clinician-reviewed free-text tasks later.

The scaffold now includes concrete seed entries for:

- Albania
- Belgium
- Sweden
- Greece
- Norway
- Spain
- France
- Italy
- Poland with LEK, LDEK, and PES exam tracks

## Commands

List registered datasets:

```bash
python -m euromedeval list-datasets
```

Show one dataset config:

```bash
python -m euromedeval show-dataset smdt-sv
```

Build one dataset locally:

```bash
python -m euromedeval build-dataset smdt-sv
```

Build all registered datasets:

```bash
python -m euromedeval build-all
```

GitHub Pages:

- `docs/index.html` is a static landing page
- `docs/site.css` and `docs/site.js` contain the site styling and motion
- enable GitHub Pages with `Build and deployment -> Source -> Deploy from a branch`
- set `Branch` to `main` and `/docs`

Preview the site locally:

```bash
python3 -m http.server 8000 -d docs
```

## Contributing

Start here:

- [Contributing Guide](/Users/birger/Documents/Papers/EuroMedEval/CONTRIBUTING.md)
- [New Dataset Guide](/Users/birger/Documents/Papers/EuroMedEval/NEW_DATASET_GUIDE.md)
- [Methodology](/Users/birger/Documents/Papers/EuroMedEval/docs/methodology.md)
- [European Seed Datasets](/Users/birger/Documents/Papers/EuroMedEval/docs/datasets/european_seed_set.md)
- [Albanian Datasets](/Users/birger/Documents/Papers/EuroMedEval/docs/datasets/albanian.md)
- [Belgian Datasets](/Users/birger/Documents/Papers/EuroMedEval/docs/datasets/belgian.md)
- [Greek Datasets](/Users/birger/Documents/Papers/EuroMedEval/docs/datasets/greek.md)

## License

This scaffold is released under the MIT License. Individual datasets may have their own licenses and access restrictions.
