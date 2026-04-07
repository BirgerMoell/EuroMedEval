# European seed datasets

This page tracks the first real datasets that can anchor EuroMedEval across countries.

## Included now

- Sweden: `smdt-sv`, `se-em-sv`, `se-gp-sv`, `pubmedqa-sv` from [Swedish Medical Benchmark](https://github.com/BirgerMoell/swedish-medical-benchmark)
- Greece: `doatap-med-el` from [Greek Medical MCQA](https://huggingface.co/datasets/ilsp/medical_mcqa_greek)
- Norway: `normedqa-no` from [NorMedQA](https://huggingface.co/datasets/SimulaMet/NorMedQA)
- Spain: `head-qa-es` from [HEAD-QA](https://huggingface.co/datasets/dvilares/head_qa)
- France: `frenchmedmcqa-fr` from [FrenchMedMCQA](https://huggingface.co/datasets/qanastek/frenchmedmcqa)
- Italy: `medschool-test-it` from [Test Medicina](https://huggingface.co/datasets/room-b007/test-medicina)
- Poland: `lek-pl`, `ldek-pl`, `pes-pl` from the [Polish medical exams collection](https://huggingface.co/collections/amu-cai/polish-english-medical-datasets-68e63489911f969816e76b05)

## Candidate but not fully integrated yet

- Albania: official medicine-profile exam material looks promising, but should be kept separate from doctor-qualification tracks

## Special handling

- Spain: `casimedicos-es` is supported as extractive QA and should be reported separately from native MCQ aggregates
- Poland: `pes-pl` should support specialty-aware reporting instead of a single undifferentiated pooled leaderboard
- Poland: `ldek-pl` is dentistry-specific and should not be merged blindly into physician-only aggregate scores

## Selection rule

Contributors should prefer datasets that satisfy as many of these conditions as possible:

- native language
- real exam or clinically reviewed educational source
- clear provenance
- reproducible reconstruction
- explicit license or public terms
- stable answer key

## What not to over-prioritize

Translated benchmarks are still welcome, but they should support comparison and calibration rather than dominate the main language leaderboard.
