# Italian datasets

## Current seed datasets

- `medschool-test-it`: [Test Medicina](https://huggingface.co/datasets/room-b007/test-medicina)
- `miur-clinica-it`: [MIUR area clinica](https://huggingface.co/datasets/Detsutut/miur-medicina-clinica)
- `miur-preclinica-it`: [MIUR area pre-clinica](https://huggingface.co/datasets/Detsutut/miur-medicina-preclinica)
- `medexpqa-it`: [MedExpQA](https://huggingface.co/datasets/HiTZ/MedExpQA)

## Why it is included

Test Medicina gives EuroMedEval an Italian native exam source with real national exam style questions. It is useful even though it is not a pure physician licensing benchmark.

The MIUR clinical and pre-clinical datasets are even stronger native sources because they are official question banks for the physician state exam.

The Italian `MedExpQA` split is included only as a bronze multilingual anchor, not as native-first flagship evidence.

## Current EuroMedEval status

- `medschool-test-it`: `medical-knowledge-mcq`, `silver`, `unofficial`, `script-only`
- `miur-clinica-it`: `clinical-case-mcq`, `gold`, `official`, `permissioned`
- `miur-preclinica-it`: `medical-knowledge-mcq`, `gold`, `official`, `permissioned`
- `medexpqa-it`: `clinical-case-mcq`, `bronze`, `unofficial`, `script-only`

## Notes

The current ingestion scripts export:

- the native Italian admission-style test as the main benchmark track
- the official MIUR physician state exam tracks as permissioned native benchmarks
- the Italian `MedExpQA` split as a bronze multilingual anchor
