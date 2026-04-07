# Contributing to EuroMedEval

Thanks for helping build a clinically useful benchmark for Europe.

## What we welcome

- new datasets
- framework improvements
- documentation
- reproducibility fixes
- clinician review for existing datasets

## Ground rules

- Native medical datasets are preferred over translated ones.
- Every dataset contribution must include provenance and licensing information.
- Do not submit private or copyrighted exam material unless you have permission to use it.
- Official leaderboard datasets need stronger review and stability than unofficial ones.

## Dataset contribution checklist

Each dataset PR should include:

1. A creation script in `src/scripts/`
2. A config entry in `src/euromedeval/dataset_configs/`
3. Documentation in `docs/datasets/`
4. Provenance and license details
5. A note on whether the dataset is `gold`, `silver`, or `bronze`
6. A note on whether it is `official` or `unofficial`
7. A small test or validation check where possible

## Framework contribution checklist

- Keep dependencies light unless there is a strong reason not to.
- Prefer typed dataclasses and straightforward APIs.
- Avoid tying the framework to one model provider.
- Preserve reproducibility and transparent reporting.

## Pull requests

Please include:

- what changed
- why it matters
- whether the change affects scoring or leaderboard comparability
- whether any dataset licensing assumptions were made

## Maintainer model

The project should grow with two review layers:

- core maintainers for framework and scoring
- language/domain maintainers for dataset quality and medical context

