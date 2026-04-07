# French datasets

## Current seed datasets

- `frenchmedmcqa-fr`: [FrenchMedMCQA](https://huggingface.co/datasets/qanastek/frenchmedmcqa)
- `mediqal-fr`: [MediQAl](https://huggingface.co/datasets/ANR-MALADES/MediQAl)
- `mediqal-oeq-fr`: [MediQAl OEQ](https://huggingface.co/datasets/ANR-MALADES/MediQAl)
- `medexpqa-fr`: [MedExpQA](https://huggingface.co/datasets/HiTZ/MedExpQA)

## Why it is included

The French seed set is now stronger because it combines a smaller open MCQ resource with a larger clinical-exam benchmark and a multilingual anchor:

- native-language
- exam-style
- open on Hugging Face
- includes a large clinical-case exam resource in `MediQAl`

## Current EuroMedEval status

- `frenchmedmcqa-fr`: `medical-knowledge-mcq`, `silver`, `unofficial`, `script-only`
- `mediqal-fr`: `clinical-case-mcq`, `gold`, `official`, `script-only`
- `mediqal-oeq-fr`: `clinical-case-qa`, `gold`, `official`, `script-only`
- `medexpqa-fr`: `clinical-case-mcq`, `bronze`, `unofficial`, `script-only`

## Notes

The current EuroMedEval exports keep:

- the single-answer subset of `FrenchMedMCQA`
- the `mcqu` subset of `MediQAl`
- the `oeq` split of `MediQAl` as a separate generative QA track
- the French `MedExpQA` split as a bronze multilingual anchor

This keeps the first French benchmark pass aligned with the current scoring spine while leaving room for future multi-answer and open-ended tracks.
