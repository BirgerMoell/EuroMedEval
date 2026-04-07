# Italian datasets

## Current seed datasets

- `medschool-test-it`: [Test Medicina](https://huggingface.co/datasets/room-b007/test-medicina)
- `medexpqa-it`: [MedExpQA](https://huggingface.co/datasets/HiTZ/MedExpQA)

## Why it is included

Test Medicina gives EuroMedEval an Italian native exam source with real national exam style questions. It is useful even though it is not a pure physician licensing benchmark.

The Italian `MedExpQA` split is included only as a bronze multilingual anchor, not as native-first flagship evidence.

## Current EuroMedEval status

- `medschool-test-it`: `medical-knowledge-mcq`, `silver`, `unofficial`, `script-only`
- `medexpqa-it`: `clinical-case-mcq`, `bronze`, `unofficial`, `script-only`

## Notes

The current ingestion scripts export:

- the native Italian admission-style test as the main benchmark track
- the Italian `MedExpQA` split as a bronze multilingual anchor
