# European seed datasets

This page tracks the first real datasets that can anchor EuroMedEval across countries.

## Included now

- Sweden: `smdt-sv`, `se-em-sv`, `se-gp-sv`, `pubmedqa-sv` from [Swedish Medical Benchmark](https://github.com/BirgerMoell/swedish-medical-benchmark)
- Norway: `normedqa-no` from [NorMedQA](https://huggingface.co/datasets/SimulaMet/NorMedQA)
- Spain: `head-qa-es` from [HEAD-QA](https://huggingface.co/datasets/dvilares/head_qa)
- France: `frenchmedmcqa-fr` from [FrenchMedMCQA](https://huggingface.co/datasets/qanastek/frenchmedmcqa)
- Italy: `medschool-test-it` from [Test Medicina](https://huggingface.co/datasets/room-b007/test-medicina)

## Candidate but not fully integrated yet

- Poland: native LEK-style public source still needs a legally clear reproducible pipeline

## Special handling

- Spain: `casimedicos-es` is supported as extractive QA and should be reported separately from native MCQ aggregates

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
