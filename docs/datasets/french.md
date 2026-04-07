# French datasets

## Current seed datasets

- `frenchmedmcqa-fr`: [FrenchMedMCQA](https://huggingface.co/datasets/qanastek/frenchmedmcqa)
- `mediqal-fr`: [MediQAl](https://huggingface.co/datasets/ANR-MALADES/MediQAl)

## Why it is included

The French seed set is now stronger because it combines a smaller open MCQ resource with a much larger clinical-exam benchmark:

- native-language
- exam-style
- open on Hugging Face
- includes a large clinical-case exam resource in `MediQAl`

## Current EuroMedEval status

- `frenchmedmcqa-fr`: `medical-knowledge-mcq`, `silver`, `unofficial`, `script-only`
- `mediqal-fr`: `clinical-case-mcq`, `gold`, `official`, `script-only`

## Notes

The current EuroMedEval exports keep:

- the single-answer subset of `FrenchMedMCQA`
- the `mcqu` subset of `MediQAl`

This keeps the first French benchmark pass aligned with the current scoring spine while leaving room for future multi-answer and open-ended tracks.
