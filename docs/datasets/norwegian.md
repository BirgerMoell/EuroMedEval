# Norwegian datasets

## Current seed dataset

- `normedqa-no`: [NorMedQA](https://huggingface.co/datasets/SimulaMet/NorMedQA)

## Why it is included

NorMedQA is a strong founding Norwegian dataset because it is:

- native-language
- medically focused
- reconstructable from a public dataset card
- published with a clear `CC BY 4.0` license

## Current EuroMedEval status

- task: `medical-knowledge-mcq`
- tier: `gold`
- status: `official`
- access mode: `script-only`

## Notes

The current ingestion script is conservative and only exports rows that can be mapped cleanly into a multiple-choice schema with a valid label.
