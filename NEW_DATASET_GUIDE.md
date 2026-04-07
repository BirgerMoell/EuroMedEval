# New Dataset Guide

This guide is for contributors adding a new dataset to EuroMedEval.

## Step 1: Decide if the dataset fits the project

The best dataset candidates are:

- medical licensing exams
- residency entrance exams
- specialist exams
- clinically reviewed case-vignette datasets

Translated benchmarks are welcome as anchor datasets, but should be clearly labeled as translated.

When scouting new countries, use this order of preference:

- official national exam questions
- reconstructable public exam archives
- specialist society question banks with public access
- clinician-reviewed educational datasets with stable answer keys

## Step 2: Check legal status

Every dataset must declare one of these access modes:

- `open`: raw or processed data can be redistributed
- `script-only`: users reconstruct the dataset locally from a public source
- `permissioned`: the evaluator is open, but raw data access is restricted

If the legal status is unclear, open an issue before spending time on the full contribution.

## Step 3: Create a processing script

Add a script under `src/scripts/`, for example:

- `create_smdt_sv.py`
- `create_lek_pl.py`

The script should:

- load the raw source
- normalize it into the EuroMedEval schema
- write a local JSONL file or prepare a dataset package
- avoid embedding private credentials or private data
- use `record_format` that matches the source, instead of squeezing QA data into MCQ

## Step 4: Add a config entry

Add a `DatasetConfig` entry in the matching language module under:

`src/euromedeval/dataset_configs/`

## Step 5: Document the dataset

Add or update a language page in `docs/datasets/` with:

- source and provenance
- task type
- country and language
- native vs translated status
- license and access mode
- intended leaderboard status

If the dataset does not fit the current record schema well, document it in `docs/datasets/european_seed_set.md` as a future candidate instead of forcing it into the wrong task family.

## Step 6: Pick status carefully

Use:

- `official` for reviewed, stable, reproducible datasets
- `unofficial` for promising datasets still being validated

## Step 7: Add a validation test if possible

At minimum, validate:

- labels are in range
- option counts are consistent
- metadata fields are present
- QA references exist when the record is not MCQ
