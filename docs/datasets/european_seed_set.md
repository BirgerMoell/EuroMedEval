# European seed datasets

This page tracks the first real datasets that can anchor EuroMedEval across countries.

## Included now

- Albania: `entrance-al-sq`, `entrance-al-systems-sq`, `entrance-al-chemistry-sq` from [Albanian medical entrance exam pools](https://huggingface.co/datasets/marjpri/albanian-medical-exams-cycles-mcq-190)
- Belgium: `entrance-be-nl` from [Belgian physician entrance exam](https://huggingface.co/datasets/jjzha/belgian-entrance-exam-physician)
- Germany: `impp-sample-de` from the official [IMPP Medizin Beispielaufgaben](https://www.impp.de/pruefungen/medizin/beispielaufgaben.html)
- Sweden: `smdt-sv`, `se-em-sv`, `se-gp-sv`, `pubmedqa-sv` from [Swedish Medical Benchmark](https://github.com/BirgerMoell/swedish-medical-benchmark)
- Greece: `doatap-med-el` from [Greek Medical MCQA](https://huggingface.co/datasets/ilsp/medical_mcqa_greek)
- Norway: `normedqa-no` from [NorMedQA](https://huggingface.co/datasets/SimulaMet/NorMedQA)
- Spain: `head-qa-es` from [HEAD-QA](https://huggingface.co/datasets/dvilares/head_qa)
- France: `frenchmedmcqa-fr`, `mediqal-fr`, `mediqal-oeq-fr`, `medexpqa-fr` from [FrenchMedMCQA](https://huggingface.co/datasets/qanastek/frenchmedmcqa), [MediQAl](https://huggingface.co/datasets/ANR-MALADES/MediQAl), and [MedExpQA](https://huggingface.co/datasets/HiTZ/MedExpQA)
- Italy: `medschool-test-it`, `miur-clinica-it`, `miur-preclinica-it`, `medexpqa-it` from [Test Medicina](https://huggingface.co/datasets/room-b007/test-medicina), [MIUR clinica](https://huggingface.co/datasets/Detsutut/miur-medicina-clinica), [MIUR preclinica](https://huggingface.co/datasets/Detsutut/miur-medicina-preclinica), and [MedExpQA](https://huggingface.co/datasets/HiTZ/MedExpQA)
- Poland: `lek-pl`, `ldek-pl`, `pes-pl` from the [Polish medical exams collection](https://huggingface.co/collections/amu-cai/polish-english-medical-datasets-68e63489911f969816e76b05)

## Candidate but not fully integrated yet

- Germany: official state-exam sample tasks are integrated, but fuller exam coverage still needs a legally cleaner route than the restricted IMPP sample release
- Portugal: native medicine entrance or residency sources would be high-value if we can secure a reproducible public pipeline
- Romania: the national rezidentiat exam remains a high-priority target once a stable public archive or reuse-cleared extraction path is found

## Special handling

- Spain: `casimedicos-es` is supported as extractive QA and should be reported separately from native MCQ aggregates
- France: `mediqal-oeq-fr` should be reported as a separate generative QA track
- France and Italy: `medexpqa-fr` and `medexpqa-it` are multilingual anchor datasets derived from parallel source material and should not affect native-only flagship scores
- Belgium: `entrance-be-nl` is an entrance exam and should not be mixed with physician qualification scores
- Albania: `entrance-al-sq` is an entrance exam and should not be mixed with physician qualification scores
- Germany: `impp-sample-de` is based on official example tasks and should be treated as a manual, sample-only German source family rather than a full German leaderboard
- Italy: `miur-clinica-it` and `miur-preclinica-it` are permissioned native datasets because the Hugging Face copies require accepted access terms
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
